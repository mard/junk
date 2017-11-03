namespace UploaderConfigurator
{
    partial class MainMenu
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.uiListboxProfiles = new System.Windows.Forms.ListBox();
            this.uiBtnAdd = new System.Windows.Forms.Button();
            this.uiBtnEdit = new System.Windows.Forms.Button();
            this.uiBtnRemove = new System.Windows.Forms.Button();
            this.uiBtnClose = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // uiListboxProfiles
            // 
            this.uiListboxProfiles.FormattingEnabled = true;
            this.uiListboxProfiles.Location = new System.Drawing.Point(12, 14);
            this.uiListboxProfiles.Name = "uiListboxProfiles";
            this.uiListboxProfiles.Size = new System.Drawing.Size(191, 134);
            this.uiListboxProfiles.TabIndex = 0;
            // 
            // uiBtnAdd
            // 
            this.uiBtnAdd.Location = new System.Drawing.Point(209, 14);
            this.uiBtnAdd.Name = "uiBtnAdd";
            this.uiBtnAdd.Size = new System.Drawing.Size(75, 23);
            this.uiBtnAdd.TabIndex = 1;
            this.uiBtnAdd.Text = "Add...";
            this.uiBtnAdd.UseVisualStyleBackColor = true;
            this.uiBtnAdd.Click += new System.EventHandler(this.uiBtnAdd_Click);
            // 
            // uiBtnEdit
            // 
            this.uiBtnEdit.Location = new System.Drawing.Point(209, 43);
            this.uiBtnEdit.Name = "uiBtnEdit";
            this.uiBtnEdit.Size = new System.Drawing.Size(75, 23);
            this.uiBtnEdit.TabIndex = 2;
            this.uiBtnEdit.Text = "Edit...";
            this.uiBtnEdit.UseVisualStyleBackColor = true;
            // 
            // uiBtnRemove
            // 
            this.uiBtnRemove.Location = new System.Drawing.Point(209, 73);
            this.uiBtnRemove.Name = "uiBtnRemove";
            this.uiBtnRemove.Size = new System.Drawing.Size(75, 23);
            this.uiBtnRemove.TabIndex = 3;
            this.uiBtnRemove.Text = "Remove";
            this.uiBtnRemove.UseVisualStyleBackColor = true;
            // 
            // uiBtnClose
            // 
            this.uiBtnClose.Location = new System.Drawing.Point(209, 125);
            this.uiBtnClose.Name = "uiBtnClose";
            this.uiBtnClose.Size = new System.Drawing.Size(75, 23);
            this.uiBtnClose.TabIndex = 4;
            this.uiBtnClose.Text = "Close";
            this.uiBtnClose.UseVisualStyleBackColor = true;
            // 
            // MainMenu
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(296, 160);
            this.Controls.Add(this.uiBtnClose);
            this.Controls.Add(this.uiBtnRemove);
            this.Controls.Add(this.uiBtnEdit);
            this.Controls.Add(this.uiBtnAdd);
            this.Controls.Add(this.uiListboxProfiles);
            this.Name = "MainMenu";
            this.Text = "PasteConfig";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ListBox uiListboxProfiles;
        private System.Windows.Forms.Button uiBtnAdd;
        private System.Windows.Forms.Button uiBtnEdit;
        private System.Windows.Forms.Button uiBtnRemove;
        private System.Windows.Forms.Button uiBtnClose;
    }
}

