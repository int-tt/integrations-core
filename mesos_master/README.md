# Mesos_master Check

This check collects metrics for Mesos masters. If you are looking for the the metrics for Mesos slave, see the [Mesos Slave Integration documentation][7].

![Mesos master Dashboard][1]

## Overview

This check collects metrics from Mesos masters for:

* Cluster resources
* Slaves registered, active, inactive, connected, disconnected, etc
* Number of tasks failed, finished, staged, running, etc
* Number of frameworks active, inactive, connected, and disconnected

And many more.
## Setup
### Installation
The installation is the same on Mesos with and without DC/OS.
Run the datadog-agent container on each of your Mesos master nodes:

```
docker run -d --name datadog-agent \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -e DD_API_KEY=<YOUR_DATADOG_API_KEY> \
  -e MESOS_MASTER=true \
  -e MARATHON_URL=http://leader.mesos:8080 \
  datadog/agent:latest
```

Substitute your Datadog API key and Mesos Master's API URL into the command above.

### Configuration

If you passed the correct Master URL when starting datadog-agent, the Agent is already using a default `mesos_master.d/conf.yaml` to collect metrics from your masters; you don't need to configure anything else. See the [sample mesos_master.d/conf.yaml][2] for all available configuration options.

Unless your masters' API uses a self-signed certificate. In that case, set `disable_ssl_validation: true` in `mesos_master.d/conf.yaml`.

### Log Collection

Datadog Agent version 6 and greater can collect logs from containers. You can either collect all logs from all your containers or filter them by container image name or container label to cherry pick what logs should be collected.

Add those extra variables to the Datadog Agent run command to start collecting logs:

* `-e DD_LOGS_ENABLED=true`: this enables the log collection when set to `true`. The Agent now looks for log instructions in configuration files or container labels
* `-e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true`: this enables log collection for all containers
* `-v /opt/datadog-agent/run:/opt/datadog-agent/run:rw`: this mounts the directory the Agent uses to store pointers on each container logs to track what have been sent to Datadog or not.

This gives the following command:

```
docker run -d --name datadog-agent \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -v /opt/datadog-agent/run:/opt/datadog-agent/run:rw \
  -e DD_API_KEY=<YOUR_DATADOG_API_KEY> \
  -e MESOS_MASTER=true \
  -e MARATHON_URL=http://leader.mesos:8080 \
  -e DD_LOGS_ENABLED=true \
  -e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \
  datadog/agent:latest
```

Use the [autodiscovery feature][3] for logs to override the `service` and `source` attribute to make sure you benefit from the integration automatic setup.

### Validation

In Datadog, search for `mesos.cluster` in the Metrics Explorer.

## Data Collected
### Metrics

See [metadata.csv][4] for a list of metrics provided by this integration.

### Events
The Mesos-master check does not include any events.

### Service Checks

`mesos_master.can_connect`:

Returns CRITICAL if the Agent cannot connect to the Mesos Master API to collect metrics, otherwise OK.

## Troubleshooting
Need help? Contact [Datadog support][5].

## Further Reading

* [Installing Datadog on Mesos with DC/OS][6]


[1]: https://raw.githubusercontent.com/DataDog/integrations-core/master/mesos_master/images/mesos_dashboard.png
[2]: https://github.com/DataDog/integrations-core/blob/master/mesos_master/datadog_checks/mesos_master/data/conf.yaml.example
[3]: https://docs.datadoghq.com/logs/log_collection/docker/#option-2-autodiscovery
[4]: https://github.com/DataDog/integrations-core/blob/master/mesos_master/metadata.csv
[5]: https://docs.datadoghq.com/help
[6]: https://www.datadoghq.com/blog/deploy-datadog-dcos
[7]: https://docs.datadoghq.com/integrations/mesos/#mesos-slave-integration
