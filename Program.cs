using System;
using System.Runtime.InteropServices;
using System.Drawing;
using System.Drawing.Imaging;

namespace dofus_move_bot
{
    class Program
    {
        static void Main(string[] args)
        {
            ScreenCapture sc = new ScreenCapture();

            Image img = sc.CaptureScreen();
            
            // capture this window, and save it
            sc.CaptureWindowToFile((IntPtr) 0x008306D8, "C:\\Users\\Erwan\\Desktop\\test.jpeg",ImageFormat.Jpeg);
        }
    }
}
