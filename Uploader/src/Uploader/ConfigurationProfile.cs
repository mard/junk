using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using IniParser;

namespace Uploader
{
    public class ConfigurationProfile : Configuration
    {
        public string Hostname { get; set; }
        public string Username { get; set; }
        public string Password { get; set; }
        public string Encryption { get; set; }
        public string EncryptionImplicit { get; set; }
        public string ForceEncryption { get; set; }
        public string RemoteDir { get; set; }
        public string Mode { get; set; }
        public string ClipboardURL { get; set; }
        public string SshHostKey { get; set; }
        public string Soundfile { get; set; }
        public string SoundEnabled { get; set; }
        public string ClipboardEnabled { get; set; }

        public void LoadProfile(string path)
        {
            IniData data = new IniData();
            if (!Path.HasExtension(path))
            {
                var storedprofile = Path.Combine(Globals.DefaultProfileDirectory, string.Concat(path, ".ini"));
                if (File.Exists(storedprofile))
                {
                    path = storedprofile;
                }
                else
                {
                    throw new FileNotFoundException("Relative profile not found.", storedprofile);
                }
            }
            else if (path.Equals(Globals.DefaultProfileFile) && !File.Exists(path))
            {
                // create if not exist
                if (!Directory.Exists(Path.GetDirectoryName(path)))
                {
                    Log.LogMessage(string.Format("Profile directory not found. Creating profile directory..."));
                    Directory.CreateDirectory(Path.GetDirectoryName(path));
                    Log.LogMessage(string.Format("Profile directory created at {0}", Path.GetDirectoryName(path)));
                }
                Log.LogMessage(string.Format("Default profile does not exist. Creating new default profile in {0}...", path));
                data.Sections.AddSection("Profile");
                data["Profile"].AddKey("Hostname");
                data["Profile"].AddKey("Username");
                data["Profile"].AddKey("Password");
                data["Profile"].AddKey("Encryption");
                data["Profile"].AddKey("EncryptionImplicit");
                data["Profile"].AddKey("ForceEncryption");
                data["Profile"].AddKey("RemoteDir");
                data["Profile"].AddKey("Mode");
                data["Profile"].AddKey("ClipboardURL");
                data["Profile"].AddKey("ClipboardEnabled");
                data["Profile"].AddKey("SshHostKey");
                data["Profile"].AddKey("Soundfile");
                data["Profile"].AddKey("SoundEnabled");
                parser.SaveFile(path, data);
                Log.LogMessage("Default profile created.");
                Console.WriteLine("Default profile created. You'll probably want to edit credentials. Program will now exit.");
                Environment.Exit(0);
            }
            else if (!File.Exists(path))
            {
                throw new FileNotFoundException("Profile not found.", Path.GetFullPath(path));
            }

            try
            {
                data = Load(path);
            }
            catch (ParsingException)
            {
                throw;
            }
            ConfigurationProfile profile = new ConfigurationProfile();
            try
            {
                Encryption = data["Profile"]["Encryption"];
                EncryptionImplicit = data["Profile"]["EncryptionImplicit"];
                ForceEncryption = data["Profile"]["ForceEncryption"];
                Hostname = data["Profile"]["Hostname"];
                Username = data["Profile"]["Username"];
                Password = data["Profile"]["Password"];
                RemoteDir = data["Profile"]["RemoteDir"];
                Mode = data["Profile"]["Mode"];
                ClipboardURL = data["Profile"]["ClipboardURL"];
                ClipboardEnabled = data["Profile"]["ClipboardEnabled"];
                SshHostKey = data["Profile"]["SshHostKey"];
                Soundfile = data["Profile"]["Soundfile"];
                SoundEnabled = data["Profile"]["SoundEnabled"];
            }
            catch (NullReferenceException)
            {
                throw new FileLoadException("Profile is corrupted.");
            }
        }
    }
}
