using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;

using swisstopo.geodesy.reframe.silverlight;

namespace ExampleApplication
{
    public partial class MainPage : UserControl
    {
        public MainPage()
        {
            InitializeComponent();
        }

        private void btnTest_Click(object sender, RoutedEventArgs e)
        {

            Reframe objReframe = new Reframe();

            double east = Double.Parse(txtE.Text);
            double north = Double.Parse(txtN.Text);
            double height = Double.Parse(txtH.Text);

            try
            {
                bool outsideChenyx06 = !objReframe.ComputeReframe(ref east, ref north, ref height,
                    Reframe.PlanimetricFrame.LV03_Military, Reframe.PlanimetricFrame.LV95, Reframe.AltimetricFrame.LN02, Reframe.AltimetricFrame.LHN95);

                txtEOut.Text = east.ToString("0.000");
                txtNOut.Text = north.ToString("0.000");
                txtHOut.Text = height.ToString("0.000");
            }
            catch (ArgumentOutOfRangeException ex)
            {
                // Input cooridnates are outsie HTRANS/CHGEO2004 perimeter (Swiss TLM) and the height transformation cannot be computed!
                MessageBox.Show("REFRAME error: " + ex.Message);
            }
            catch (Exception)
            {
                // Other error e.g. transformation's dataset file not found (swisstopo.data.dll)
                MessageBox.Show("REFRAME internal error, please reinstall application.");
            }

        }

    }
}
