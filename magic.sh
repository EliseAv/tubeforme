#!/bin/bash
#
# Copyright 2008-2015, Ekevoo.com.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#

function falar () {
    echo "[[ $* ]]"
    osascript -e "display notification \"$*\" with title \"Magic\""
    #echo "Falando: $*"
    #espeak -p 70 -s 120 -v brazil "$@" 2>/dev/null &
}

echo '==========================' $$
date
falar 'Fila de vídeos: iniciando.'
cd "$( dirname "${BASH_SOURCE[0]}" )"

# SINGLE-INSTANCE - esse script não pode ter várias cópias rodando
PIDFILE=".pid"
PID2=`cat "$PIDFILE"`
if [ -n "$PID2" ] && [ $(ps ax | grep "^ *$PID2 " | wc -l) -gt 0 ]; then
    echo "$0 já rodando no pid $PID2. Abortando."
    pstree -p "$PID2"
    falar 'Processo pendurado. Fila de vídeos abortada.'
    echo '=========================='
    exit
fi
echo $$ > "$PIDFILE"

# SOURCE - essa é a parte que vai na fonte e busca itens novos
./pull.py

# DEDUPLICATE - o pull é meio fominha…
./dedup.py save

# WIFI SENTINEL - somente baixar quando tiver na rede certa
if [ "`uname`" == "Darwin" ]; then
    ssid=$(/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/ {print substr($0, index($0, $2))}')
    if [ "$ssid" != "RaccoonNet" ]; then
        exit
    fi
fi

# SINK - essa é a parte que fica baixando tudo
ATTEMPTS=10
mkdir -p videos
cd videos
while [ -s ../queue.txt ]
do
    ../youtube-dl \
        --write-description \
        --no-progress \
        -cita ../queue.txt 2>&1
        #-f bestvideo+bestaudio \
    ../dedup.py save
    ATTEMPTS=$(( $ATTEMPTS - 1 ))
    if [ $ATTEMPTS -lt 1 ]; then break; fi
done

VIDEOS=(*)
NUM=$(( ${#VIDEOS[*]} / 2 ))
if  [ $NUM -gt 1 ]; then MSG="$NUM vídeos em fila."; fi

echo
echo ">>> $MSG"
falar "$MSG"
DISPLAY=:0 XAUTHORITY=~/.Xauthority notify-send "$MSG" 2>/dev/null
date

##exit 0
## PENDRIVE - a parte de levar os vídeos!
#P=/mnt
#D=$P/queue
#mount $P
#if [ -d $D/videos ]
#then
#	mv -v * $D/videos/
#	cd ../prabaixar && mv -v $D/prabaixar/* .
#	cd ../pmv && mv -v $D/pmv/* .
#	cd ..
#	if [ -s  $D/queue.txt ]; then
#		cat   $D/queue.txt >> queue.txt
#		rm    $D/queue.txt
#		touch $D/queue.txt
#	fi
#	for f in magic.sh pull.py refiltra.pl youtube-dl log; do
#		if   [ $f -nt $D/$f ]; then cp -v $f $D/$f
#		elif [ $D/$f -nt $f ]; then cp -v $D/$f $f; chmod +x $f
#		fi
#	done
#	umount $P
#	sync
#	date
#fi

falar 'Fila de vídeos concluída.'
echo '=========================='
echo
