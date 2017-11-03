using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NUnit.Framework;
using Uploader;
using System.IO;
using IniParser;

namespace UploaderTests
{
    [TestFixture]
    public class Profiles
    {
        [Test]
        public void CorrectSchemaRelativePath()
        {
            var temp = new ConfigurationProfile();
            temp.LoadProfile(@"BasicProfile");
        }

        [Test]
        public void CorrectSchemaAbsolutePath()
        {
            var temp = new ConfigurationProfile();
            temp.LoadProfile(Path.Combine(Globals.DefaultProfileDirectory, @"BasicProfile"));
        }

        [Test]
        [ExpectedException(typeof(ParsingException))]
        public void IncorrectSchemaRelativePath()
        {
            var temp = new ConfigurationProfile();
            temp.LoadProfile(@"CorruptedProfile");
        }

        [Test]
        [ExpectedException(typeof(ParsingException))]
        public void IncorrectSchemaAbsolutePath()
        {
            var temp = new ConfigurationProfile();
            temp.LoadProfile(Path.Combine(Globals.DefaultProfileDirectory, @"CorruptedProfile"));
        }

        [Test]
        [ExpectedException(typeof(FileNotFoundException))]
        public void NotFoundProfileRelativePath()
        {
            var temp = new ConfigurationProfile();
            temp.LoadProfile(@"Phantom");
        }

        [Test]
        [ExpectedException(typeof(FileNotFoundException))]
        public void NotFoundProfileAbsolutePath()
        {
            var temp = new ConfigurationProfile();
            temp.LoadProfile(Path.Combine(Path.GetTempPath(), "derp.ini"));
        }
    }
}
