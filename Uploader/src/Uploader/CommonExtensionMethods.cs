using System;
using System.Text;

namespace Uploader
{
    public static class CommonExtensionMethods
    {
        public static bool IsTrue(this string value)
        {
            switch (value)
            {
                case "1":
                case "true":
                case "on":
                case "yes":
                case "enabled":
                    return true;
                default:
                    return false;
            }
        }
    }   
}
