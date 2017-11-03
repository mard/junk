using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Windows.Forms;

namespace Uploader
{
    class Log
    {
        public static void LogConsole(string message)
        {
            Console.WriteLine(message);
            WriteToFile(message);
        }

        public static void LogMessage(string message)
        {
            WriteToFile(message);
        }

        public static void LogException(Exception e, string extra = null)
        {
            Console.WriteLine(e.Message);
            //Console.WriteLine(e);
            if (extra != null) Console.WriteLine(extra);
            WriteToFile(e.Message);
        }

        private static void WriteToFile(string message)
        {
            File.AppendAllText(Path.Combine(Globals.ExecutableDirectory, "log.txt"), string.Format("{0} - {1}{2}", DateTime.Now, message, Environment.NewLine));
        }
    }
}
