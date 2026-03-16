module.exports = {
  apps : [
    {
      name: "love-meter-server",
      script: "server.js",
      cwd: "/home/pop/.openclaw/workspace/love-meter",
      watch: true,
      env: {
        NODE_ENV: "production",
      }
    },
    {
      name: "love-meter-tunnel",
      script: "ssh",
      args: "-o ServerAliveInterval=30 -R 80:localhost:8080 nokey@localhost.run",
      restart_delay: 5000,
      autorestart: true
    }
  ]
};
