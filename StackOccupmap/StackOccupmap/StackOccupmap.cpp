#include <Windows.h>

void * __cdecl malloc(unsigned int bytes)
{
	return HeapAlloc(GetProcessHeap(), 0, bytes);
}

void __cdecl free(void *ptr)
{
	if (ptr) HeapFree(GetProcessHeap(), 0, ptr);
}

struct OccupMap
{
	size_t _size;
	int* _data;

	OccupMap(size_t size, int ival=0)
	{
		_data = (int*)malloc(sizeof(int) * size);
		for(size_t i = 0 ; i < size ; i++)
		{
			_data[i] = ival;
		}
		_size = size;
	}
	~OccupMap()
	{
		free(_data);
	}
	int& operator[](int index) { return _data[index]; }
	size_t size() const { return _size; }

	int* begin() { return _data; }
	int* end() { return _data + _size; }
};


extern "C" {
	__declspec(dllexport) void _cdecl StackOccupmaps(OccupMap occupList[], size_t* ret, int size) {
		size_t maxMergedOccupmapSize = 0;
		for (int i = 0; i < size; i++)
		{
			const auto& occupMap = occupList[i];
			maxMergedOccupmapSize += occupMap.size();
		}
		OccupMap mergedOccupMap(maxMergedOccupmapSize + 1, -1);

		size_t lastAllocatedPos = 0;

		for (int i = 0; i < size; i++)
		{
			auto& occupMap = occupList[i];
			auto occupMapSize = occupMap.size();

			size_t j;

			// preprocess dwoccupmap
			for (j = 0; j < occupMapSize; j++) {
				if (occupMap[j] == 0) occupMap[j] = -1;
				else if (j == 0 || occupMap[j - 1] == -1) occupMap[j] = j;
				else occupMap[j] = occupMap[j - 1];
			}

			// Find appropriate position to allocate object
			j = 0;
			while (j < occupMapSize) {
				if (occupMap[j] != -1 && mergedOccupMap[lastAllocatedPos + j] != -1) {
					lastAllocatedPos = mergedOccupMap[lastAllocatedPos + j] - occupMap[j];
					j = 0;
				}
				else j++;
			}

			for (j = occupMapSize - 1; j != -1; j--) {
				int currentOffset = lastAllocatedPos + j;
				if (occupMap[j] != -1 || mergedOccupMap[currentOffset] != -1)
				{
					if (mergedOccupMap[currentOffset + 1] == -1)
						mergedOccupMap[currentOffset] = currentOffset + 1;
					else
						mergedOccupMap[currentOffset] = mergedOccupMap[currentOffset + 1];
				}
			}
			ret[i] = (lastAllocatedPos << 2);
		}
	}


	// DLL Entry
	BOOL APIENTRY _DllMainCRTStartup(HMODULE hModule, DWORD fdwReason, LPVOID lpReserved)
	{
		switch (fdwReason)
		{
		case DLL_PROCESS_ATTACH:
			break;
		case DLL_PROCESS_DETACH:
			break;
		case DLL_THREAD_ATTACH:
			break;
		case DLL_THREAD_DETACH:
			break;
		}
		return TRUE;
	}

}

