using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using IniParser;
using System.IO;
using AlexPilotti.FTPS.Client;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;

namespace Uploader
{
    class Upload
    {
        //private string hostname, username, password;

        public static void UploadFiles(ConfigurationProfile profile, string temppath, string remotedir)
        {
            // Setup session options
            // add support for: scp/sftp protocols, ssh host/private keys, active/passive mode, port, FtpSecure, timeout, ssl cert, 

            using (FTPSClient session = new FTPSClient())
            {
                
                ESSLSupportMode sslSupportMode = ESSLSupportMode.ClearText;
                RemoteCertificateValidationCallback userValidateServerCertificate;
                userValidateServerCertificate = new RemoteCertificateValidationCallback(ValidateServerCertificate);

                // enable encryption if desired
                if (profile.Encryption.IsTrue())
                {
                    sslSupportMode |= ESSLSupportMode.ControlAndDataChannelsRequired | ESSLSupportMode.CredentialsRequired;
                    if (profile.EncryptionImplicit.IsTrue())
                    {
                        // implicit if desired
                        sslSupportMode |= ESSLSupportMode.Implicit;
                    }
                    if (profile.ForceEncryption.IsTrue())
                    {
                        // force encryption if desired
                        userValidateServerCertificate = new RemoteCertificateValidationCallback(delegate { return true; });
                    }
                }

                session.Connect(profile.Hostname, new System.Net.NetworkCredential(profile.Username, profile.Password), sslSupportMode, userValidateServerCertificate);

                // Upload files
                //TransferOptions transferOptions = new TransferOptions();
                //transferOptions.TransferMode = TransferMode.Binary;

                //TransferOperationResult transferResult;
                //transferResult = session.PutFiles(Path.Combine(temppath, "*"), Common.Parse(remotedir), false, transferOptions);

                try
                {
                    session.SetCurrentDirectory(Common.ParseTemplate(remotedir));
                }
                catch
                {
                    session.MakeDir(Common.ParseTemplate(remotedir));
                }
                session.PutFiles(temppath, Common.ParseTemplate(remotedir), "*", EPatternStyle.Wildcard, false, new FileTransferCallback(TransferCallback));

                // Throw on any error
                //transferResult.Check();

                // Print results
                //foreach (TransferEventArgs transfer in transferResult.Transfers)
                //{
                //    Console.WriteLine("Upload of {0} succeeded", transfer.FileName);
                //}
            }
        }

        private static void TransferCallback(FTPSClient sender, ETransferActions action, string localObjectName, string remoteObjectName, ulong fileTransmittedBytes, ulong? fileTransferSize, ref bool cancel)
        {
            switch (action)
            {
                case ETransferActions.FileDownloaded:
                case ETransferActions.FileUploaded:
                    //OnFileTransferCompleted(fileTransmittedBytes, fileTransferSize);
                    break;
                case ETransferActions.FileDownloadingStatus:
                case ETransferActions.FileUploadingStatus:
                    //OnFileTransferStatus(action, localObjectName, remoteObjectName, fileTransmittedBytes, fileTransferSize);
                    break;
                case ETransferActions.RemoteDirectoryCreated:
                    //if (options.verbose)
                    {
                        Console.WriteLine();
                        Console.WriteLine("Remote directory created: " + remoteObjectName);
                    }
                    break;
                case ETransferActions.LocalDirectoryCreated:
                    //if (options.verbose)
                    {
                        Console.WriteLine();
                        Console.WriteLine("Local directory created: " + localObjectName);
                    }
                    break;
            }
        }

        public static bool ValidateServerCertificate(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            if (sslPolicyErrors == SslPolicyErrors.None)
            {
                return true;
            }
            return false;
        }

    }
}
