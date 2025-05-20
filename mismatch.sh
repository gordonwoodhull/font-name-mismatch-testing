#! /usr/bin/env bash

# takes names of fonts on stdin and prints the css name, fc-scan name, and typst name
# outputs font-names.csv google-fonts,typst
echo "google,typst" > font-names.csv
while read -r line; do
  #echo $line
  deq=`echo $line | sed 's:^"::' | sed 's:"$::'`
  echo -e "$deq\tgoogle-fonts"
  unsp=`echo $deq | sed 's: \(..\):%20\1:g'`
  cssurl="https://fonts.googleapis.com/css?family=$unsp"
  #echo $url
  css=`curl -s $cssurl`
  #echo $css
  fam=`echo "$css" | grep font-family | sed "s/  font-family: '//" | sed "s/';//"`
  echo -e "$fam\tcss"
  fonturl=`echo $css | grep -w src | sed 's:.*url(\([^)]*\)).*:\1:'`
  if [ -n "$fonturl" ]; then
    curl -s -O $fonturl
    fontfile=`echo $fonturl | sed 's:.*/\([^/]*\)$:\1:'`
    #echo $fontfile
    fcs=`fc-scan  --format "%{family}" "./$fontfile"`
    echo -e "$fcs\tfc-scan"
    mkdir -p test
    mkdir -p done
    mv ./$fontfile test/
    typst=`quarto typst fonts --ignore-system-fonts --font-path test/ 2>&1 | grep -v 'DejaVu Sans Mono' | grep -v 'Libertinus Serif' | grep -v 'New Computer Modern'`
    echo -e "$typst\ttypst"
    mv test/$fontfile done/$fontfile
    if [ "$deq" != "$typst" ]; then
      echo "$deq,$typst" >> font-names.csv
    fi
    echo
  fi
  sleep 1
done
