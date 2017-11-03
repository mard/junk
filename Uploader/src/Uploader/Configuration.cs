using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using IniParser;
using System.IO;

namespace Uploader
{
    abstract public class Configuration
    {
        internal FileIniDataParser parser;

        public Configuration()
        {
            parser = new FileIniDataParser();
        }

        internal IniData Load(string path)
        {
            parser = new FileIniDataParser();
            IniData data = new IniData();
            try
            {
                data = parser.LoadFile(path);
            }
            catch (ParsingException e)
            {
                throw e.InnerException;
            }
            return data;
        }
    }
}
