using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Uploader
{
    class Links : List<string>
    {
        public void ToClipboard(ConfigurationProfile profile)
        {
            if (profile.ClipboardEnabled.IsTrue())
            {
                var text = this.ToArray().Aggregate((a, b) => string.Format("{0}{1}{2}", a, Environment.NewLine, b));
                System.Windows.Forms.Clipboard.SetText(text);
            }
        }
    }
}
