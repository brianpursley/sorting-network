#!/bin/bash

pushd "$(dirname "$0")" > /dev/null || exit 1

FAILED_TEST_COUNT=0

test_failed() {
  echo -e "\e[31mfailed\e[0m"
  FAILED_TEST_COUNT=$((FAILED_TEST_COUNT + 1))
}

test_passed() {
  echo -e "\e[32mok\e[0m"
}

echo -e "Running CLI tests...\n"

echo -n "check: from file ... "
ACTUAL=$(../sortingnetwork.py -i ../examples/3-input.cn check)
ACTUAL_EXIT_CODE=$?
EXPECTED="It is a sorting network!"
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "check: from stdin ... "
ACTUAL=$(../sortingnetwork.py check < ../examples/3-input.cn)
ACTUAL_EXIT_CODE=$?
EXPECTED="It is a sorting network!"
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "check: negative ... "
ACTUAL=$(echo "0:1,1:2,2:3" | ../sortingnetwork.py check)
ACTUAL_EXIT_CODE=$?
EXPECTED="It is not a sorting network."
EXPECTED_EXIT_CODE=1
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "check: show progress ... "
ACTUAL=$(../sortingnetwork.py -i ../examples/3-input.cn check --show-progress)
ACTUAL_EXIT_CODE=$?
EXPECTED=$(echo -e "\rChecking... 0%\rIt is a sorting network!")
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "print: to stdout ... "
ACTUAL=$(echo "0:1,1:2,0:1" | ../sortingnetwork.py print)
ACTUAL_EXIT_CODE=$?
EXPECTED=$(echo -e "0:1\n1:2\n0:1\n")
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "print: to file ... "
TEMP_FILE=$(mktemp)
echo "0:1,1:2,0:1" | ../sortingnetwork.py print "$TEMP_FILE"
ACTUAL_EXIT_CODE=$?
ACTUAL=$(cat "$TEMP_FILE")
EXPECTED=$(echo -e "0:1\n1:2\n0:1\n")
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi
rm "$TEMP_FILE"

echo -n "sort ... "
ACTUAL=$(../sortingnetwork.py -i ../examples/3-input.cn sort 3,1,2)
ACTUAL_EXIT_CODE=$?
EXPECTED=$(echo -e "1\n2\n3\n")
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "svg: to stdout ... "
ACTUAL=$(../sortingnetwork.py -i ../examples/3-input.cn svg)
ACTUAL_EXIT_CODE=$?
EXPECTED=$(cat ../examples/3-input.svg)
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi

echo -n "svg: to file ... "
TEMP_FILE=$(mktemp)
../sortingnetwork.py -i ../examples/3-input.cn svg "$TEMP_FILE"
ACTUAL_EXIT_CODE=$?
ACTUAL=$(cat "$TEMP_FILE")
EXPECTED=$(cat ../examples/3-input.svg)
EXPECTED_EXIT_CODE=0
if [ "$ACTUAL" != "$EXPECTED" ] || [ $ACTUAL_EXIT_CODE -ne $EXPECTED_EXIT_CODE ]; then
  test_failed
else
  test_passed
fi
rm "$TEMP_FILE"

if [ $FAILED_TEST_COUNT -gt 0 ]; then
  echo -e "\n\e[31m$FAILED_TEST_COUNT test(s) failed.\e[0m"
  exit 1
else
  echo -e "\n\e[32mOK\e[0m"
fi

popd > /dev/null || exit 1
