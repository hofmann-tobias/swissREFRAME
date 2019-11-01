using System;
using System.Collections.Generic;
using System.Text;

using swisstopo.geodesy.reframe; // REFRAME namespace

namespace ReframeSampleCS
{
    class Program
    {
        static void Main(string[] args)
        {
            // Instantiate Reframe object
            Reframe reframeObj = new Reframe();

            // Input point (LV03)
            // Write your code here, e.g. to read a file
            double east = 600100.000, north = 200100.000, height = 500.000;

            try
            {
                // Log
                Console.WriteLine("REFRAME input: E: " + east.ToString("0.000") + " m / N: " + north.ToString("0.000") + " m / H: " + height.ToString("0.000") + " m");

                // Compute Reframe transfromation LV03 (MI)=>LV95 and LN02=>LHN95
                bool outsideChenyx06 = !reframeObj.ComputeReframe(ref east, ref north, ref height,
                    Reframe.PlanimetricFrame.LV03_Military, Reframe.PlanimetricFrame.LV95,
                    Reframe.AltimetricFrame.LN02, Reframe.AltimetricFrame.LHN95);

                if (outsideChenyx06)
                    Console.WriteLine("This point is outside official Swiss TLM perimeter. A translation +2'000'000.0/+1'000'000.0 was applied.");

                // Show message
                Console.WriteLine("REFRAME transformation terminated: E: " + east.ToString("0.000") + " m / N: " + north.ToString("0.000") + " m / H: " + height.ToString("0.000") + " m");
            }
            catch (ArgumentOutOfRangeException e)
            {
                // Input cooridnates are outsie HTRANS/CHGEO2004 perimeter (Swiss TLM) and the height transformation cannot be computed!
                Console.WriteLine("REFRAME error: " + e.Message);
            }
            catch (Exception)
            {
                // Other error e.g. transformation's dataset file not found (swisstopo.data.dll)
                Console.WriteLine("REFRAME internal error, please reinstall application.");
            }

            // Let time to read screen messages
            System.Threading.Thread.Sleep(5000);
        }
    }
}
