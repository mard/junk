using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using IniParser;
using System.IO;

namespace Uploader
{
    public class ConfigurationGeneral : Configuration
    {
        public string Portable { get; set; }

        public ConfigurationGeneral LoadGeneral(string path)
        {
            IniData data = new IniData();
            try
            {
                data = Load(path);
            }
            catch (FileNotFoundException)
            {
                Log.LogMessage(string.Format("Configuration does not exist. Creating new configuration in {0}...", path));
                data.Sections.AddSection("General");
                data["General"].AddKey("Portable");
                data["General"]["Portable"] = "1";
                parser.SaveFile(path, data);
                Log.LogMessage(string.Format("Configuration created.", path));
            }
            ConfigurationGeneral configuration = new ConfigurationGeneral();
            configuration.Portable = data["General"]["Portable"];
            return configuration;
        }
    }
}
