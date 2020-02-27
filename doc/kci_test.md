## `kci_test`

The output of `kci_build` can be used with `kci_test` to generate and submit
test definitions.  It will be using the meta-data JSON files produced by
`kci_build` and will also need to communicate with the test labs where to run
the tests.  Currently, only [LAVA](https://www.lavasoftware.org/) is fully
supported but other types of lab can be added.  Test configurations can be
found in
[`test-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/master/test-configs.yaml)
with the list of test plans and which devices should run them.  Likewise, the
lab configurations can be found in
[`lab-configs.yaml`](https://github.com/kernelci/kernelci-core/blob/master/lab-configs.yaml).

Each lab is expected to have a remote API available with a URL and a user
authentication token.

For example, using the build output from the commands shown in the `kci_build`
section, to generate and submit tests in a lab:

### 1. Optional: save a local copy of lab specific data

Generating a test definition can rely on some information that can only be
provided by the lab where it needs to be submitted.  For example, some labs
have specific names for their device types.  Retrieving this information every
time a job definition is generated can have a significant overhead while in
practice this information doesn't change very often.

To avoid repeating the same queries with the labs, the `kci_test get_lab_info`
can be used to store it locally in a JSON file and then reuse it with other
commands.  This is mostly useful when running automated jobs that will
determine when to get the information again (say, once for each kernel revision
being built, or once every hour...).  When submitting only a few jobs manually,
the overhead may not be so much of a problem.

Here's a sample command to get the data from a lab and store it in a JSON file:
```
./kci_test get_lab_info \
  --lab=lab-name \
  --lab-json=lab-name.json \
  --user=kernelci-user-name \
  --token=abcd-7890
```

### 2. Generate test definitions

The `kci_test generate` command will generate test definitions for a given set
of build meta-data and a given lab.  It can either generate all the compatible
test definitions based on the `test_config` entries in `test-configs.yaml`, or
a subset of it, or a single arbitrary one specified on the command line.

The `--callback-id` and `--callback-url` options are only used to get a
callback from the test lab to a service who can receive it.  It is not required
to generate and run a job, if the results can be shared by other means or
manually inspected.

To generate the definitions of all the jobs that can be run in a lab:
```
./kci_test generate \
  --bmeta-json=linux/_install_/bmeta.json \
  --dtbs-json=linux/_install_/dtbs.json \
  --lab-json=lab-name.json \
  --storage=https://some-storage-place.com/ \
  --lab=lab-name \
  --user=kernelci-user-name \
  --token=abcd-7890 \
  --output=jobs \
  --callback-id=kernelci-callback \
  --callback-url=https://callback-recipient.com/handler/
```

Extra options can be added to only generate a subset of those jobs, filtering
by test plan, target or machine type:
```
--plan=baseline
```
```
--target=odroid-xu3
```
```
--mach=qemu
```

To generate only one job definition with an arbitrary combination of test plan
and target, even if it is not listed in any `test_config` entry:
```
./kci_test generate
  --bmeta-json=linux/_install_/bmeta.json \
  --dtbs-json=linux/_install_/dtbs.json \
  --plan=baseline_qemu \
  --target=qemu_arm64-virt-gicv3 \
  --lab=lab-name \
  --user=kernelci-user-name \
  --token=abcd-7890 \
  --lab-json=lab-name.json \
  --storage=https://some-storage-place.com/ \
  --callback-id=kernelci-callback-local \
  --callback-url=https://callback-recipient.com/handler/ \
  > job.yaml
```

### 3. Submit tests

Once the test job definitions have been generated and stored in some files,
they can be submitted to the test lab:

```
./kci_test submit \
  --lab=lab-name \
  --user=kernelci-user-name \
  --token=abcd-7890 \
  --jobs=jobs/*
```
