for name in $(ls -al $MYBORG_LBIN); do
    [ -f $MYBORG_LBIN/$name ] && echo $name
done
