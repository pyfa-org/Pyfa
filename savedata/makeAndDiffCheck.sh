#!/bin/bash
if [[ $2 == -v ]] ; then
    MUTE=False
else
    MUTE=TRUE
fi
EXPECTERRORS=False
if [[ $3 == --search ]] ; then
    if [[ $5 == --expect-errors ]] ; then
        EXPECTERRORS=True
    fi
else
    if [[ $3 == --expect-errors ]] ; then
        EXPECTERRORS=True
    fi
fi
if [[ $1 == -f ]] ; then
    if [[ $MUTE == TRUE ]] ; then
        python3opt savedata/efs_util.py\ -f | grep awgahwogfa
    else
        python3opt savedata/efs_util.py\ -f\ --search=$4
    fi
elif [[ $1 == -b ]] ; then
    if [[ $MUTE == TRUE ]] ; then
        python3opt savedata/efs_util.py\ -b | grep awgahwogfa
    else
        python3opt savedata/efs_util.py\ -b\ --search=$4
    fi
elif [[ $1 == -u ]] ; then
    if [[ $MUTE == TRUE ]] ; then
        python3opt savedata/efs_util.py\ -b\ -f\ -o\ .. | grep awgahwogfa
    else
        python3opt savedata/efs_util.py\ -b\ -f\ -o\ ..
    fi
elif [[ $1 == -a ]] ; then
    if [[ $MUTE == TRUE ]] ; then
        python3opt savedata/efs_util.py\ -b\ -f | grep awgahwogfa
    else
        python3opt savedata/efs_util.py\ -b\ -f\ --search=$4
    fi
else
    echo Defaulting to fits and base ships.\n
    if [[ $MUTE == TRUE ]] ; then
        python3opt savedata/efs_util.py\ -b\ -f | grep awgahwogfa
    else
        python3opt savedata/efs_util.py\ -b\ -f\ --search=$4
    fi
fi
if [[ $EXPECTERRORS == True ]] ; then
    echo Expecting non standard output, this should only be used for testing
else
diff -s --color=always ../shipJSON.js ~/.pyfa/shipJSON.js | grep -m 3 --color ''
diff -s --color=always ../shipBaseJSON.js ~/.pyfa/shipBaseJSON.js | grep -m 3 --color ''
/home/stock/scripts/Pyfa/.tox/pep8/bin/flake8 --exclude=.svn,CVS,.bzr,.hg,.git,__pycache__,venv,tests,.tox,build,dist,__init__.py,floatspin.py --ignore=E121,E126,E127,E128,E203,E731,F401,E722,E741 service/efsPort.py --max-line-length=165
fi
