#include <iostream>
#include <cstring>

using namespace std;

extern "C" {
	const size_t N = 80;
	int length;
	char str[N];
	char newstr[N];
};

int main()
{
	cout << "Input your text:" << endl;
	fgets(str, N, stdin);

	length = strlen(str);
	__asm(R"(
		.intel_syntax noprefix
		xor ecx, ecx
		mov esi, length
		dec esi

		loop:
		mov eax, str[esi]
		mov newstr[ecx], al

		inc ecx
		dec esi

		cmp esi, 0
		jge loop
		.att_syntax
	)");

	cout << "Your result text:";
	for(int i=0; i<length; i++) cout<<newstr[i];
	cout<<"\n";

	return 0;
}
