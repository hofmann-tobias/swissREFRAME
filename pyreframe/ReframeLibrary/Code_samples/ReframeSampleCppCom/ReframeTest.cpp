#import <swisstopoReframeLib.tlb>

#include <iostream>

inline void pause();

int main()
{
	// Declarations
	double east, north, height;

	// Ask/read coordinates to transform
	std::cout << std::endl << "Input east: ";
	std::cin >> east;
	std::cout << std::endl <<"Input north: ";
	std::cin >> north;
	std::cout << std::endl <<"Input height: ";
	std::cin >> height;

	try
	{
		// Initialize COM connection
		CoInitialize(NULL);

		// Create a pointer to the Reframe class from DLL
		swisstopoReframeLib::IReframePtr pReframe(__uuidof(swisstopoReframeLib::Reframe));

		// Transform LV03 coordinates to LV95 and LN02 height to Bessel
		int result = pReframe->ComputeReframe(&east, &north, &height, 0, 1, 0, 2);

		if (result == 1)
		{
			std::cout << "Transformation successful (return code: " << result << ")" << std::endl;
			std::cout.precision(3);
			std::cout << std::fixed << "E: " << east << " m / N: " << north << " m / H: " << height << " m" << std::endl;

			pause();
			return 0;
		}
		else
		{
			std::cout << "Transformation failed!" << std::endl;
			std::cout << "Return code: " << result << std::endl;
			pause();
			return 1;
		}
	}
	catch (std::runtime_error re)
	{
		std::cout << "Reframe error: " << re.what() << std::endl;
		pause();
		return 1;
	}
	catch (...)
	{
		std::cout << "Internal error: COM initialization failed or REFRAME COM library not found" << std::endl;
		pause();
		return 1;
	}
}

void pause()
{
	std::cin.ignore();//Ignores previous input, get cin.get working even with new line inputs.
	std::cin.get();
}