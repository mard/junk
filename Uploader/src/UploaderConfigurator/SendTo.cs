using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using IWshRuntimeLibrary;
using System.Diagnostics;

namespace UploaderConfigurator
{
    class SendTo
    {
        public static void List()
        {
            string sendto = Environment.GetFolderPath(Environment.SpecialFolder.SendTo);

            List<string> files = new List<string>();
            var a = Directory.GetFiles(sendto).Where(i => Path.GetExtension(i).Equals(".lnk")).ToList();

            IWshShell shell = new WshShell();
            IWshShortcut link = (IWshShortcut)shell.CreateShortcut(a[0]);

            Debug.WriteLine(link.TargetPath);
            Debug.WriteLine(link.WorkingDirectory);
        }
    }
}
