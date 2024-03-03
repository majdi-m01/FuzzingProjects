#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include "include/libxml/tree.h"
#include "include/libxml/parser.h"

#define SIZE 1000

void harness(char* buffer, ssize_t length) {
	const char dummy_xml_name[] = "noname.xml";
	xmlDocPtr doc = xmlReadMemory(buffer, length, dummy_xml_name, NULL, 0);
	if (doc != NULL) {
		xmlFreeDoc(doc);
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
