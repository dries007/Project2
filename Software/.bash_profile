[[ -f ~/.bashrc ]] && . ~/.bashrc

# Terminal resize
[[ $TERM != "screen" ]] && resize 45 180

getLocalIP() {
    local _ip _myip _line _nl=$'\n'
    while IFS=$': \t' read -a _line ;do
        [ -z "${_line%inet}" ] &&
           _ip=${_line[${#_line[1]}>4?1:2]} &&
           [ "${_ip#127.0.0.1}" ] && _myip=$_ip
      done< <(LANG=C /sbin/ifconfig)
    printf ${1+-v} $1 "%s${_nl:0:$[${#1}>0?0:1]}" $_myip
}

echo "Hostname: `hostname`"
echo "Local IP: `getLocalIP`"
echo "Date: `date`"
echo "HwClock: `hwclock`"

runApp() {
    echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
    www/app.py
}

export APP_GCAL_ID=""
export APP_GCAL_SECRET=""
export SDL_FBDEV=/dev/fb1

[ "$TERM" != "screen" ] && [ "$SSH_TTY" == "" ] && runApp
