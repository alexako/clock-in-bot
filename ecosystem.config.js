module.exports = {
  apps : [{
    script: 'run_server.sh',
    watch: '.',
    ignore_watch: ["__pycache__"],
  }],
};
