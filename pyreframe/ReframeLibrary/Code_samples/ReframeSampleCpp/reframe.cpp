#include <iostream>
#include <sstream>
#include <Windows.h>
#include "reframe.h"

int main()
{
	// Input coordinates to transform
	double east = 640000.0, north = 184000.0, height = 530.0;

	try
	{
		// ReframeWrapper object
		ReframeWrapper reframeLibObj;

		// Process coordinate transformation LV03->LV95, LN02->Bessel
		bool outsideChenyx06 = !reframeLibObj.ComputeReframe(east, north, east, ReframeWrapper::LV03_Military, ReframeWrapper::LV95, ReframeWrapper::LN02, ReframeWrapper::Ellipsoid);

		// Message if outside CHENyx06
		if (outsideChenyx06)
			std::cout << "Input coordinates are outside Swiss TLM perimeter: a translation has been applied!" << std::endl;

		// Write results to console
		std::cout << "REFRAME transformation terminated: " << std::endl;

		// Format outputs (3 decimals)
		char buffer[100];
		sprintf_s(buffer, "%.3lf", east); std::string sEast = buffer;
		sprintf_s(buffer, "%.3lf", north); std::string sNorth = buffer;
		sprintf_s(buffer, "%.3lf", height); std::string sHeight = buffer;
		std::cout << "E: " << sEast << " m / N: " << sNorth << " m / H: " << sHeight << " m" << std::endl;

		Sleep(5000);

		return 0;
	}
	catch (std::runtime_error re)
	{
		std::cout << "REFRAME error: " << re.what() << std::endl;

		Sleep(5000);

		return 1;
	}
	catch (...)
	{
		std::cout << "Internal error: impossible to load ReframeWrapper" << std::endl;

		Sleep(5000);

		return 1;
	}
}