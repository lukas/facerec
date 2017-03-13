until lt --port 5000 -s $TUNNELNAME; do
    echo 'lt crashed... respawning...'
    sleep 1
done
