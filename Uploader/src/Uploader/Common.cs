using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using System.IO;

namespace Uploader
{
    class Common
    {
        public static string ParseTemplate(string text)
        {
            return text
                .Replace("{yyyy}", DateTime.Now.ToString("yyyy"))
                .Replace("{MM}", DateTime.Now.ToString("MM"));
        }

        public static void CreateTemporaryDirectory()
        {
            if (!Directory.Exists(Globals.TemporaryDirectory))
            {
                Directory.CreateDirectory(Globals.TemporaryDirectory);
            }
        }

        public static void DeleteTemporaryDirectory()
        {
            if (Directory.Exists(Globals.TemporaryDirectory))
            {
                foreach (var file in Directory.GetFiles(Globals.TemporaryDirectory))
                {
                    FileAttributes attributes = File.GetAttributes(file);
                    if ((attributes & FileAttributes.ReadOnly) == FileAttributes.ReadOnly)
                    {
                        File.SetAttributes(file, attributes & ~FileAttributes.ReadOnly);
                    }
                    File.Delete(file);
                }
                Directory.Delete(Globals.TemporaryDirectory);
            }
        }

        public static void PlaySound(ConfigurationProfile profile)
        {
            if (profile.SoundEnabled.IsTrue())
            {
                using (var p = new System.Media.SoundPlayer())
                {
                    p.SoundLocation = Path.Combine(Globals.ExecutableDirectory, profile.Soundfile);
                    p.PlaySync();
                }
            }
        }
    }
}
