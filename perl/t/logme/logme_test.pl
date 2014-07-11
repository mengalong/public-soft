#!/usr/bin/env perl
use strict;
use FindBin qw($Bin);
use File::Basename;
use Cwd "abs_path";
use Data::Dumper;
use lib "$Bin/../../publib";
use Logme::Logme;

my $progname = __FILE__;
my $CURRENT_PATH = dirname(abs_path(__FILE__));
my %loginfo = (
        "logProg" => "$progname",
        "bindir" => "$Bin",
        "logdir" => "$CURRENT_PATH/log",
        "wf" => "$CURRENT_PATH/log/$progname.log.wf",
        "nt" => "$CURRENT_PATH/log/$progname.log",
        "log_debug" => 1,
        "printStd" => 1,
        "log_detail" => {
                "NOTICE" => 0,
                "DEBUG" => 1,
                "WARNNING" => 2,
                "FATAL" => 3,
        },
        "log_maxSize" => 200000000,
        "log_minLine" => 10000,
);

my $logit = new Logme::Logme(%loginfo);

my %logstr = (
	"desc" => "test log info",
	"subkey" => "testkey",
);

$logit->printLog($logit->{NOTICE},\%logstr);
$logit->printLog($logit->{WARNNING},\%logstr);
$logit->printLog($logit->{FATAL},\%logstr);
