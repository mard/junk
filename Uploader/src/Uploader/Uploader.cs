using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;
using System.IO;
using System.Windows.Forms;
using System.Web;
using System.Diagnostics;
using System.Threading;
using System.Linq;
using IniParser;

namespace Uploader
{
    class Uploader
    {
        [STAThread]
        static void Main(string[] args)
        {
            // Registering handler for unhandled exceptions
            AppDomain.CurrentDomain.UnhandledException += UnhandledExceptionHandler;

            // Fetching global configuration
            var general = new ConfigurationGeneral();
            general.LoadGeneral(Globals.SettingsFile);

            // Fetching data from command-line arguments
            var argumentdata = new ArgumentData(args);

            // Create temporary directory for copied files.
            Common.CreateTemporaryDirectory();

            // List of URLs to be copied to clipboard.
            Links links = new Links();

            for (int i = argumentdata.Files.Count - 1; i >= 0; i--)
            {
                var filename = Path.GetFileName(argumentdata.Files[i]);

                var currentclipboardurl = Common.ParseTemplate(argumentdata.Profile.ClipboardURL).Replace("%file%", HttpUtility.UrlPathEncode(filename));
                links.Add(currentclipboardurl);

                var newfilename = Path.Combine(Globals.TemporaryDirectory, filename);
                File.Copy(argumentdata.Files[i], newfilename, true);

                // TODO: touch or not? Store this preference in profile configuration
                System.IO.File.SetLastWriteTimeUtc(newfilename, DateTime.UtcNow.AddSeconds(i));
            }

            if (Directory.GetFileSystemEntries(Globals.TemporaryDirectory).Length > 0)
            {
                Upload.UploadFiles(argumentdata.Profile, Globals.TemporaryDirectory, argumentdata.Profile.RemoteDir);

                links.ToClipboard(argumentdata.Profile);
                Common.PlaySound(argumentdata.Profile);
            }
            Common.DeleteTemporaryDirectory();
            Environment.Exit(0);
        }

        static void UnhandledExceptionHandler(object sender, UnhandledExceptionEventArgs e)
        {
            Exception ex = (Exception)e.ExceptionObject;
            Log.LogMessage(e.ExceptionObject.ToString());
            Common.DeleteTemporaryDirectory();
            Environment.Exit(1);
        }
    }
}
