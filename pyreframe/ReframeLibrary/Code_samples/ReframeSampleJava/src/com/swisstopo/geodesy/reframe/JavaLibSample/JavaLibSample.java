package com.swisstopo.geodesy.reframe.JavaLibSample;

import com.swisstopo.geodesy.reframe_lib.*;
import com.swisstopo.geodesy.reframe_lib.IReframe.AltimetricFrame;
import com.swisstopo.geodesy.reframe_lib.IReframe.PlanimetricFrame;
import com.swisstopo.geodesy.reframe_lib.IReframe.ProjectionChange;

public class JavaLibSample {

	public static void main(String[] args) {
		
        // REFRAME object
        Reframe reframeObj = new Reframe();
	
		double[] inputCoordinates = new double[] { 540000.0, 260000.0, 600.0  };
		System.out.println(String.valueOf(inputCoordinates[0]) + " / " + String.valueOf(inputCoordinates[1]) + " / " + String.valueOf(inputCoordinates[2]));
		try
		{
			double[] outputCoordinates = reframeObj.ComputeReframe(inputCoordinates, PlanimetricFrame.LV03_Military, PlanimetricFrame.LV95, AltimetricFrame.LN02, AltimetricFrame.Ellipsoid);
			System.out.println(String.valueOf(outputCoordinates[0]) + " / " + String.valueOf(outputCoordinates[1]) + " / " + String.valueOf(outputCoordinates[2]));
			
			outputCoordinates = reframeObj.ComputeGpsref(outputCoordinates, ProjectionChange.LV95ToETRF93Geographic);
			System.out.println(String.valueOf(outputCoordinates[0]) + " / " + String.valueOf(outputCoordinates[1]) + " / " + String.valueOf(outputCoordinates[2]));
		}
		catch (IllegalArgumentException e)
		{
			System.out.println("Outside grid");
		}
		catch (NullPointerException e)
		{
			System.out.println("Dataset file missing");
		}
		catch (Exception e)
		{
			System.out.println("Error 2");
		}

	}
	
}
