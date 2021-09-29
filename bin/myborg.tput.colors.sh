#!/source/this/sh

export_ () { export $1=$2 ; }

# DETERMINE MY (MYBORG) LOCATION. 
# (This is written to [~/.local/var] ny the installer.)
export_ MYBORG          $(cat ~/.local/var/myborg/current.txt)

# SETUP MY SBIN AND PYTHON LIBRARY.
export_ MYBORG_SBIN     ${MYBORG}/bin
export_ PATH            ${PATH}:${MYBORG_SBIN}
export_ PYTHONPATH      ${MYBORG}/lib

# DEFINE INTERNAL PATHS.
export_ MYBORG_MANIFEST ${MYBORG}/MANIFEST
export_ MYBORG_MODS     ${MYBORG}/.mods
export_ MYBORG_BUILD    ${MYBORG}/.build
export_ MYBORG_DOTS     ${MYBORG}/dots
mkdir -p ${MYBORG_BUILD}

# DEFINE EXTERNAL PATHS

export_ MYBORG_BIN      ${HOME}/.local/var/myborg/mybin
export_ MYBORG_BUILD    ${HOME}/.local/var/myborg/mybin
export_ MYBORG_OPT      ${HOME}/.local/opt/MYBORG_OPT

# PREPARE LBIN.
export_ MYBORG_LBIN_BIN     ${MYBORG_BUILD}/lbin
export_ MYBORG_LBIN_PREFIX  ${MYBORG}/lbin
. myborg.lbin.__source__

# BE NICE.
export_ PATH            ${PATH}:${HOME}/.local/bin


main () {
    echo "++[$MYBORG/main] $*"
    echo processing index...   ; __myborg.manifest
    echo activating mods...    ; __myborg_activate
    echo borgifying...         ; __myborg_borgify $1
    echo "++[$MYBORG/main] $*"
}

red     () { printf "$(tput bold)$(tput setaf 15)$(tput setab 1)$1$(tput sgr0)" ; }
green   () { printf "$(tput bold)$(tput setaf 15)$(tput setab 2)$1$(tput sgr0)" ; }
yellow  () { printf "$(tput bold)$(tput setaf 15)$(tput setab 3)$1$(tput sgr0)" ; }
blue    () { printf "$(tput bold)$(tput setaf 15)$(tput setab 4)$1$(tput sgr0)" ; }
ok      () { printf "$(tput bold)$(tput setaf 2)$(tput setab 15)$1$(tput sgr0)" ; }

__myborg_source () {
    [ "$1" = "-q" ] || __myborg_note__ sourcing $*
    [ "$1" = "-q" ] && shift
    source $*
}
__myborg_borgify () {
    [ ! "$1" == "" ] && {
        __myborg_source borg:__first__
        __myborg_source ${MYBORG_DOTS}/dot$1
        __myborg_source borg:__last__
        __myborg_source borg:path:clean
    }
}
__myborg_activate () {
    for name in $(ls ${MYBORG_MODS} | sort); do
        path=${MYBORG_MODS}/$name
        [ -f ${path}/.insitu/activate ] || {
            printf "[skip] \t[$name]\n"
            continue
        }
        printf "[ ok ] \t[$name]\n"
        > /dev/null 2>/dev/null     pushd $path/.insitu
        . ./activate
        > /dev/null 2>/dev/null     popd
    done
}
__myborg_note__ () {
    printf "$1:\t" ; shift ; printf "[$*]" ; echo
}
main $*
