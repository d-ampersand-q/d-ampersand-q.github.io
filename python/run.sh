for i in `ls python/ | grep article | sed -e 's/[.]py$//'`; do echo $i; python ./python/$i.py > blogs/$i.html; done
