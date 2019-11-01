#pragma comment(lib, "..\\References\\ReframeLibWrapper.lib")

class __declspec(dllimport) ReframeWrapper
{
public:
	// Enums / reference frames
	enum PlanimetricFrame
	{
		LV03_Military = 0,
		LV95 = 1,
		LV03_Civil = 2,
	};
	enum AltimetricFrame
	{
		LN02 = 0,
		LHN95 = 1,
		Ellipsoid = 2,
		CHGeo98 = 3
	};
	enum ProjectionChange
	{
		ETRF93GeocentricToLV95 = 0,
		ETRF93GeographicToLV95 = 1,
		LV95ToETRF93Geocentric = 2,
		LV95ToETRF93Geographic = 3
	};

	// Initialization
	ReframeWrapper();
	virtual ~ReframeWrapper();

	// Methods
    bool ComputeReframe(double &east, double &north, double &height, PlanimetricFrame plaFrameIn, PlanimetricFrame plaFrameOut, AltimetricFrame altFrameIn, AltimetricFrame altFrameOut);
    void ComputeGpsref(double &east_x_lon, double &north_y_lat, double &height_z, ProjectionChange transformation);

private:
	// Pointer to REFRAME library object
	void* m_pReframeClr;
};
