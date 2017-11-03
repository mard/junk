using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NUnit.Framework;
using Uploader;
using System.IO;

namespace UploaderTests
{
    [TestFixture]
    public class Arguments
    {
        [Test]
        [ExpectedException(typeof(ArgumentException))]
        public void NotEnoughParameters()
        {
            string[] args = new string[]{};
            new ArgumentData(args);
        }

        [Test]
        public void FileNotFound()
        {
            string[] args = new string[] {"john"};
            new ArgumentData(args);
        }

        [Test]
        public void FilesNotFound()
        {
            string[] args = new string[] { "eric", "terry", "michael" };
            new ArgumentData(args);
        }

        [Test]
        public void ProfileNotSpecified()
        {
            string[] args = new string[] { "/profile" };
            new ArgumentData(args);
        }

        [Test]
        public void CorrectProfileButNoFiles()
        {
            string[] args = new string[] { "/profile", "BasicProfile" };
            new ArgumentData(args);
        }

        [Test]
        public void FileNotFoundCorrectProfile()
        {
            string[] args = new string[] { "/profile", "BasicProfile", "graham" };
            new ArgumentData(args);
        }

        [Test]
        public void FilesNotFoundCorrectProfile()
        {
            string[] args = new string[] { "/profile", "BasicProfile", "john", "terry" };
            new ArgumentData(args);
        }

        [Test]
        public void ArgumentsWentWrong()
        {
            string[] args = new string[] { @"files\samplefile", "/profile" };
            new ArgumentData(args);
        }

        [Test]
        public void ArgumentsWentVeryWrong()
        {
            string[] args = new string[] { "/profile", @"files\samplefile", "/profile" };
            new ArgumentData(args);
        }
    }
}
