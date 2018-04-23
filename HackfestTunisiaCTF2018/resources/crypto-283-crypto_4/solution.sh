#!/bin/bash

command="python ../server.py" #[OR] nc 46.105.29.234 17331

git clone https://github.com/stephenbradshaw/hlextend
cd hlextend
test_user_hash=$(echo -e "1\ntest" | ${command} | grep -v username | grep ":" | cut -d":" -f2)
for i in $(seq 1 30)
do
new_username=$(python -c "import hlextend;sha = hlextend.new('sha256');print sha.extend('administrator', 'test', ${i}, '${test_user_hash}')");
new_username_hash=$(python -c "import hlextend;sha = hlextend.new('sha256');sha.extend('administrator', 'test', ${i}, '${test_user_hash}');print sha.hexdigest()");
new_username_hexencoded=$(python -c "print '${new_username}'.encode('hex')");
echo -e "2\n${new_username_hexencoded}:${new_username_hash}" | ${command};
sleep 1
done

