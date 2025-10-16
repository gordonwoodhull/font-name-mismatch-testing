#! /usr/bin/env bash

# takes names of fonts on stdin and prints the css name, fc-scan name, and typst name
# outputs font-names.csv google-fonts,typst
echo "google,typst" > font-names.csv
while read -r line; do
  # Clean up the font name (remove quotes)
  deq=`echo $line | sed 's:^"::' | sed 's:"$::'`
  echo -e "$deq\tgoogle-fonts"

  # Format the font name for URL
  unsp=`echo $deq | sed 's: \(..\):%20\1:g'`
  cssurl="https://fonts.googleapis.com/css?family=$unsp"

  # Get CSS content
  css=`curl -s $cssurl`

  # Check for font-family in CSS
  if ! echo "$css" | grep -q "font-family"; then
    echo -e "(failed)\tcss"
    echo -e "(failed)\tfc-scan"
    echo -e "(failed)\ttypst"
    echo
    sleep 1
    continue
  fi

  # Extract font family
  fam=`echo "$css" | grep font-family | sed "s/  font-family: '//" | sed "s/';//"`
  echo -e "$fam\tcss"

  # Extract font URL
  fonturl=`echo $css | grep -w src | sed 's:.*url(\([^)]*\)).*:\1:'`
  if [ -z "$fonturl" ]; then
    echo -e "(failed)\tfc-scan"
    echo -e "(failed)\ttypst"
    echo
    sleep 1
    continue
  fi

  # Download the font file
  curl -s -O $fonturl
  fontfile=`echo $fonturl | sed 's:.*/\([^/]*\)$:\1:'`

  # Check if file downloaded successfully
  if [ ! -f "./$fontfile" ]; then
    echo -e "(failed)\tfc-scan"
    echo -e "(failed)\ttypst"
    echo
    sleep 1
    continue
  fi

  # Run fc-scan
  fcs=`fc-scan --format "%{family}" "./$fontfile" 2>/dev/null`
  if [ -z "$fcs" ]; then
    echo -e "(failed)\tfc-scan"
  else
    echo -e "$fcs\tfc-scan"
  fi

  # Create directories
  mkdir -p test
  mkdir -p done

  # Move file for typst processing
  mv "./$fontfile" test/ 2>/dev/null || true

  # Run typst
  typst=`quarto typst fonts --ignore-system-fonts --font-path test/ 2>&1 | grep -v 'DejaVu Sans Mono' | grep -v 'Libertinus Serif' | grep -v 'New Computer Modern'`
  if [ -z "$typst" ]; then
    echo -e "(failed)\ttypst"
  else
    echo -e "$typst\ttypst"

    # Add to CSV if names differ
    if [ "$deq" != "$typst" ]; then
      echo "$deq,$typst" >> font-names.csv
    fi
  fi

  # Move file to done directory if it exists
  if [ -f "test/$fontfile" ]; then
    mv "test/$fontfile" "done/$fontfile" 2>/dev/null || true
  fi

  echo
  sleep 1
done
