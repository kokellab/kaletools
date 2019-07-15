import argparse, sys, re, logging
from pathlib import Path
from typing import Mapping, Any, Sequence, Collection
from typing import Tuple as Tup

logger = logging.getLogger('paperpile-latex')


class Paperpiler:

	HELP_TEXT = '''
Converts parenthetical citations formatted by paperpile-locator.csl.xml to autocite BibTeX.
Takes a text file with parenthetical citations formatted by paperpile-locator.csl.xml and a BibTeX file with supported identifiers,
and outputs (to stdout) the new text file with each {}-like citation to a LaTeX-compatible \autocite call using the labels from the Bibtex file.
The supported labels are global identifiers pointing to your specific article/book/website, minus page/section numbers. They are:
	- DOI
	- ISBN
	- PubMed ID
	- PubMed Central ID
	- URL
Every entry in your BibTeX file must have at least one of these.
This works by formatting parenthetical citations as strings of the supported identifiers surrounded by {}, which are linked to your BibTeX file.
For example, this line:
	> Toxicology {3^doi:'10.1016/j.neuro.2008.09.011`^pmid:'18952124`^url:'http://dx.doi.org/10.1016/j.neuro.2008.09.011`} {4^doi:'10.1016/j.bbr.2011.11.020`^pmid:'22138507`^url:'http://dx.doi.org/10.1016/j.bbr.2011.11.020`} and more.
Gets converted into:
	> Toxicology \autocite{MacPhail2009-dg,Ali2012-ts} and more.
I used this to help convert my Paperpile-connected Google Doc to a LaTeX file. Here are the steps:
	1. In the Google Doc, navigate to `Paperpile→View all references` and add at least a DOI, ISBN, PubMed ID, PubMed Central ID, or URL to each (more is safer).
	1. Upload `paperpile-locator.csl.xml` (in this repository) under your Paperpile "Citation styles" settings.
	2. In your Google Doc, change your formatting style to paperpile-locator.csl.xml (search for it).
	3. Choose "format citations" in the Paperpile menu (and wait for it to finish).
	4. Export the bibliography to a BibTeX file.
	5. Export your paper as a text file. (Note: I found this easier than converting to Word or HTML and using Pandoc. Pandoc balked on my files.)
	6. Run `paperpile-latex.py <path-to-text-file> <path-to-bibtex-file> --fixes`. (`--fixes` is optional, but I found it useful.)
	7. Check for any errors in the terminal.
	8. Copy the text outputted to `<path-to-text-file>.ppiled.tex` to the document section of your LaTeX template. You’ll want to remove the bibliography at the end.
Note that this has not been extensively tested. You should check your output LaTeX file.
'''
	TERMS = ['pmid', 'pmcid', 'doi', 'isbn', 'url']
	CITE_PATTERN = re.compile(r'\$?\{([0-9]+)(\^[^}]+)\}')
	ID_PATTERN = re.compile(r'\^(' + '|'.join(['(?:' + t + ')' for t in TERMS]) + r"):'([^`]+)`")
	RESERVED_CHARS = '\\ & % $ # _ ~ ^'.split(' ')  # \ must be first # also { }

	@classmethod
	def main(cls, args: Sequence[str]) -> None:
		if len(args)>0 and args[0].endswith('paperpile-latex.py'):
			args = args[1:]  # hacky
		parser = argparse.ArgumentParser(
			description=Paperpiler.HELP_TEXT,
			formatter_class=argparse.RawTextHelpFormatter
		)
		parser.add_argument('text', type=str, help='Path to the text file to convert')
		parser.add_argument('bib', type=str, help='Path to bibtex file')
		parser.add_argument('-f', '--fixes', action='store_true', help='Apply common LaTeX fixes, such as escaping reserved characters')
		parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite the output file if it exists')
		opts = parser.parse_args(args)
		ppiler = Paperpiler(Path(opts.bib), opts.fixes)
		ppiler.convert(Path(opts.text), opts.overwrite)

	def __init__(self, bib_path: Path, fixes: bool = False):
		self.bib_path = Path(bib_path)
		self.bib_dict = self._build_bib()
		self.fixes = fixes

	def convert(self, text_path: Path, overwrite: bool = False) -> None:
		text_path = Path(text_path)
		output_path = self._output_path(text_path)
		if not overwrite and output_path.exists():
			raise IOError("Path {} already exists".format(output_path))
		with text_path.open() as infile:
			text = infile.read()
		logger.info("Read {} characters from {}".format(len(text), text_path))
		fixer = self.build_replacements(text)
		text = self._apply_replacements(text, fixer)
		text = self._apply_fixes(text)
		with output_path.open('w') as outfile:
			outfile.write(text)
		logger.info("Wrote {} characters to {}".format(len(text), output_path))

	def _output_path(self, path: Path) -> Path:
		return Path(str(path) + '.paperpiled.tex')

	def _build_bib(self) -> Mapping[str, str]:
		dictionary = {}
		for doi, tag in self._iterate_bib():
			if doi in dictionary and dictionary[doi] != tag:
				logging.error("Term {} maps to both {} and {}".format(doi, dictionary[doi], tag))
			dictionary[doi] = tag
		logging.info("Found {} terms for {} papers".format(len(dictionary), len(set(dictionary.values()))))
		return dictionary

	def _iterate_bib(self) -> Tup[str, str]:
		tag, hit_one = None, True
		with self.bib_path.open() as f:
			for i, line in enumerate(f.readlines()):
				line = line.strip()
				if len(line) == 0: continue
				if line.startswith('@'):
					if not hit_one:
						logging.warning("{} has no global term/ID (one of {})".format(tag, ','.join(Paperpiler.TERMS)))
					tag = line.split('{')[1][:-1]
					hit_one = False
				elif any((line.startswith(x) for x in Paperpiler.TERMS)):
					doi = line.split('"')[1]
					hit_one = True
					yield doi, tag

	def build_replacements(self, text: str) -> Mapping[str, str]:
		fixer, cites_failed = {}, set()
		n_found = 0
		for n_found, match in enumerate(Paperpiler.CITE_PATTERN.finditer(text)):
			paper = self._find_term(match, self.bib_dict)
			if paper is None:
				assert str(match.group(0)) != 'None'
				cites_failed.add(match.group(0))
			else:
				fixer[match.group(0)] = paper
		refs_expected = set(self.bib_dict.values())
		refs_used = set(fixer.values())
		refs_missed = refs_expected - refs_used
		logger.info("Fixed {}/{} citations for {} papers".format(n_found-len(cites_failed), n_found, len(refs_used)))
		self._warn_list(refs_missed, "papers not cited")
		self._warn_list(cites_failed, "citations malformatted or not in the bibliography")
		return fixer

	def _apply_replacements(self, text: str, fixer: Mapping[str, str]) -> str:
		for key, value in fixer.items():
			text = text.replace(key, '\\autocite{' + value + '}')
		return text

	def _apply_fixes(self, text: str) -> str:
		if self.fixes:
			for r in Paperpiler.RESERVED_CHARS:
				text = text.replace(r, '\\' + r)
			# these could definitely be done better
			text = text.replace(r'} \\autocite{', ',')
			text = text.replace(r'\\autocite', r'\autocite')
			text = text.replace(r'\\ref{', r'\ref{')
			text = text.replace(r'°', r'\deg')
			text = text.replace(r'µ', r'\micro')
			text = text.replace(r'–', '--')
			text = text.replace(r'—', '---')
		text = text.replace(r'} \autocite{', ',')
		return text

	def _find_term(self, match, dictionary: Mapping[str, str]):
		for m in Paperpiler.ID_PATTERN.finditer(match.group(0)):
			if m.group(2) in dictionary:
				return dictionary[m.group(2)]
		return None

	def _warn_list(self, items: Collection[Any], info: str) -> None:
		if len(items) > 0:
			logger.error("There are {} {}:\n[\n    {}\n]".format(len(items), info, '\n    '.join([str(i) for i in items])))
		else:
			logger.info("There are 0 " + info)


if __name__ == '__main__':
	logger.setLevel(logging.INFO)
	logging.basicConfig(format="%(levelname)-8s: %(message)s")
	Paperpiler.main(sys.argv)

__all__ = ['Paperpiler']
