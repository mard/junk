using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace Uploader
{
    public class ArgumentData
    {
        public List<string> Files { get; private set; }
        public ConfigurationProfile Profile { get; private set; }

        public ArgumentData()
        {
            Files = new List<string>();
            Profile = new ConfigurationProfile();
        }

        public ArgumentData(string[] args) : this()
        {
            Parse(args);
        }

        public void Parse(string[] args)
        {
            if (args.Length == 0)
            {
                throw new ArgumentException("Not enough parameters");
            }
            for (int i = 0; i < args.Length; i++)
            {
                if (args[i].Equals("/profile") && args.Length - 1 > i)
                {
                    Profile.LoadProfile(args[i + 1]);
                }
                else if (i > 0 && !args[i - 1].Equals("/profile"))
                {
                    Files.Add(args[i]);
                }
                else if (i == 0 && !args[i].Equals("/profile"))
                {
                    Files.Add(args[i]);
                }
            }
            // Loading default profile if it's not passed by a parameter
            if (Profile.Hostname == null)
            {
                Profile.LoadProfile(Globals.DefaultProfileFile);
            }
        }
    }
}
