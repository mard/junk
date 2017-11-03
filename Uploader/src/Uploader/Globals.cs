using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Windows.Forms;
using System.Reflection;

namespace Uploader
{
    public class Globals
    {

        public static string ExecutableDirectory
        {
            get
            {
                return Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            }
        }

        public static string ExecutableName
        {
            get
            {
                return Path.GetFileNameWithoutExtension(Application.ExecutablePath);
            }
        }

        public static string DefaultProfileDirectoryName
        {
            get
            {
                return "profiles";
            }
        }

        public static string DefaultProfileDirectory
        {
            get
            {
                return Path.Combine(ExecutableDirectory, DefaultProfileDirectoryName);
            }
        }

        public static string DefaultProfileFile
        {
            get
            {
                return Path.Combine(DefaultProfileDirectory, string.Concat(ExecutableName, ".ini"));
            }
        }

        public static string SettingsFile
        {
            get
            {
                return Path.Combine(ExecutableDirectory, SettingsFilename);
            }
        }

        public static string SettingsFilename
        {
            get
            {
                return string.Concat(ExecutableName, ".ini");
            }
        }

        public static string TemporaryDirectory
        {
            get
            {
                return Path.Combine(Path.GetTempPath(), "Uploader");
            }
        }
    }
}
