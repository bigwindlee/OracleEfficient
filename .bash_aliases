alias gitlog='git log -5 --oneline'

alias mydu='du -hs * | sort -rh | head -5'

alias myssh='autossh -M 5678 -N -f -L 8090:localhost:8090 azure'
alias mynet='netstat -anop |grep 8090'

alias cd1='cd /home/feng/wanhe/tmdocs'
alias cd2='cd /home/feng/wanhe/szhj'

alias beianhe='cd /home/feng/wanhe/tmdocs; nodemon --inspect=0.0.0.0:9229 -w ./src ./src'

alias szhj1='cd /home/feng/wanhe/szhj/proj; npm run dev'
alias szhj2='cd /home/feng/wanhe/szhj/proj/client/szhj-ui; npm run serve'

# copy the latest <*.tgz> in /home/fun/backup from <azure> to local tmp directory
alias myscp='scp azure:`ssh azure "ls -rt /home/fun/backup/*.tgz" |tail -1` /tmp'

# debug mocha
alias demo='node --inspect-brk ./node_modules/mocha/bin/_mocha --require ts-node/register --timeout 9999999'
