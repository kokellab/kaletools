# helpful aliases
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias cd..='cd ..'
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'
alias xdg-open=open
alias ports='netstat -tulanp'
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'
alias wgetc='wget -c'
function cdd { mkdir "$1" && cd "$1" }
function cdd. { mkdir "../$1" && cd "../$1" }
alias brewski='brew update && brew upgrade; brew cleanup; brew doctor'
function f { if (( $# > 0 )); then open -a Finder "$1";  else open -a Finder ./; fi }
alias xdg-open=open
alias p=grealpath

