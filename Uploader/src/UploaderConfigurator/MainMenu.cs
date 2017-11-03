using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace UploaderConfigurator
{
    public partial class MainMenu : Form
    {
        public MainMenu()
        {
            InitializeComponent();
        }

        protected override void OnLoad(EventArgs e)
        {
            SendTo.List();
            base.OnLoad(e);
        }

        private void uiBtnAdd_Click(object sender, EventArgs e)
        {
            Form editor = new ProfileEditor();
            editor.ShowDialog();
        }
    }
}
