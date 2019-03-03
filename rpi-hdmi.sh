#!/bin/sh

# author/source: https://gist.github.com/quelleck/1d8fc8395fd52d4aa38a99ef46d8598e
# forked from: https://gist.github.com/AGWA/9874925

# Enable and disable HDMI output on the Raspberry Pi

is_off ()
{
	vcgencmd display_power | grep "display_power=0" >/dev/null
}

case $1 in
	off)
        	if is_off
        	then
            		echo Already off...
        	else
            		vcgencmd display_power 0
        	fi
	;;
	on)
		if is_off
		then
			vcgencmd display_power 1
        	else
            		echo Already on...
		fi
	;;
	status)
		if is_off
		then
			echo off
		else
			echo on
		fi
	;;
	*)
		echo "Usage: $0 on|off|status" >&2
		exit 2
	;;
esac

exit 0
