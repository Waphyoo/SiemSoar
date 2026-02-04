using System;
using System.Windows.Forms;
using System.Data.SqlClient;
using System.Net;

namespace VulnerableApp
{
    public partial class Form1 : Form
    {
        // ❌ Vulnerability 1: Hardcoded Credentials
        private const string ADMIN_USER = "admin";
        private const string ADMIN_PASS = "P@ssw0rd123";
        
        // ❌ Vulnerability 2: Hardcoded API Key
        private const string API_KEY = "sk_live_51HyPvx2eZvKYlo2C...";

        public Form1()
        {
            InitializeComponent();
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            string username = txtUsername.Text;
            string password = txtPassword.Text;

            // ❌ Vulnerability 3: SQL Injection
            if (CheckCredentialsInsecure(username, password))
            {
                lblStatus.Text = "Login Successful!";
                MessageBox.Show("Welcome " + username);
                
                // ❌ Vulnerability 4: Insecure HTTP API Call
                CallInsecureAPI(username);
            }
            else
            {
                lblStatus.Text = "Invalid credentials";
            }
        }

        // SQL Injection Vulnerable Function
        private bool CheckCredentialsInsecure(string user, string pass)
        {
            try
            {
                string connString = "Server=localhost;Database=testdb;Integrated Security=true;";
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    
                    // ❌ String concatenation = SQL Injection
                    string query = "SELECT * FROM Users WHERE username='" + user + "' AND password='" + pass + "'";
                    
                    SqlCommand cmd = new SqlCommand(query, conn);
                    SqlDataReader reader = cmd.ExecuteReader();
                    
                    return reader.HasRows;
                }
            }
            catch
            {
                // Simple hardcoded check as fallback
                return (user == ADMIN_USER && pass == ADMIN_PASS);
            }
        }

        // ❌ Vulnerability 5: Insecure Communication
        private void CallInsecureAPI(string username)
        {
            try
            {
                using (WebClient client = new WebClient())
                {
                    // No SSL/TLS certificate validation
                    ServicePointManager.ServerCertificateValidationCallback = 
                        (sender, certificate, chain, sslPolicyErrors) => true;
                    
                    string url = "http://api.example.com/login?user=" + username + "&key=" + API_KEY;
                    string response = client.DownloadString(url);
                }
            }
            catch { }
        }
    }
}