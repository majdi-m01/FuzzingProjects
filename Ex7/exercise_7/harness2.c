#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include "include/libxml/tree.h"
#include "include/libxml/parser.h"
#include "include/libxml/xmlregexp.h"

#define SIZE 1000

void harness(char* buffer, ssize_t length) {
    const xmlChar *pcPattern = (const xmlChar *)buffer;
	xmlRegexpPtr pRegPtr;

    if (buffer) {
        pRegPtr = xmlRegexpCompile(pcPattern);
        if (pRegPtr) {
            xmlRegFreeRegexp(pRegPtr);
        } else {
            fprintf(stderr, "Failed to compile regular expression.\n");
        }
    } else {
        fprintf(stderr, "Buffer is null.\n");
    }
}

int main(int argc, char** argv) {
	char input[SIZE];
	while (__AFL_LOOP(1000)) {
		ssize_t length = read(STDIN_FILENO, input, SIZE);
		harness(input, length);
	}
	return 0;
}