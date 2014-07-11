package Logme::Logme;
BEGIN
{
	use Exporter();
	use vars qw($VERSION @ISA @EXPORT);
	use Data::Dumper;
	use File::Basename;
	@ISA = qw(Exporter);
	@EXPORT = qw();
}

sub new {
	my $type    =   shift;
	my %param   =   @_; 
	my $this    =   {}; 
	$this->{conf}->{logdir} =   $param{logdir};
	$this->{conf}->{bindir} =   $param{bindir};
	$this->{conf}->{wf} =   $param{wf};
	$this->{conf}->{nt} =   $param{nt};
	$this->{conf}->{logProg} = $param{logProg};
	$this->{conf}->{log_debug} = $param{log_debug};
	$this->{conf}->{printStd} = $param{printStd};
	$this->{NOTICE} = $param{log_detail}->{NOTICE};
	$this->{DEBUG} = $param{log_detail}->{DEBUG};
	$this->{WARNNING} = $param{log_detail}->{WARNNING};
	$this->{FATAL} = $param{log_detail}->{FATAL};
	$this->{log_maxSize} = $param{log_maxSize};
	$this->{log_minLine} = $param{log_minLine};
	bless $this;
	return $this;
}

#打开日志文件句柄
sub openFile {
	my $this    =   shift;
	if ((! -d $this->{conf}->{logdir}) || ( ! -e $this->{conf}->{wf})
		|| ( ! -e $this->{conf}->{nt}) ) {
		my $cmd =   "mkdir -p $this->{conf}->{logdir} 2>&1 && touch $this->{conf}->{wf} $this->{conf}->{nt} 2>&1";
		my $ret =   $this->runCmd($cmd,3);
		if ($ret->{ret} != 0) {
			$ret->{desc} = "mkdir for log path failed,cmd=$cmd";
			return $ret;
		} 
	}
	if ( (-w $this->{conf}->{wf}) && (-w $this->{conf}->{nt}) ) {
		if ( ! open($this->{hd_wf}, ">>$this->{conf}->{wf}")) {
			$ret->{ret}     =   1;
			$ret->{desc}    =   "open $this->{conf}->{wf} failed";
			$ret->{cmd}     =   "openFile";
			return $ret;
		}
		if ( ! open($this->{hd_nt}, ">>$this->{conf}->{nt}")) {
			$ret->{ret}     =   1;
			$ret->{desc}    =   "open $this->{conf}->{nt} failed";
			$ret->{cmd}     =   "openFile";
			return $ret;
		}
	} else {
		$ret->{ret}     =   1;
		$ret->{desc}    =   "$this->{conf}->{wf} or $this->{conf}->{nt} Permission denied";
		$ret->{cmd}     =   "openFile";
		return $ret;
	}
	$ret->{ret}     =   0;
	$ret->{desc}    =   "open log file successed";
	$ret->{cmd}     =   "openFile";
	return $ret;
}

#关闭文件句柄
sub closeFile {
	my $this    =   shift;
	my @fileToClose = ($this->{conf}->{wf}, $this->{conf}->{nt});
	my $logFile;
	my @fstat;
	my $cmd;
	my $ret;
	foreach  $logFile (@fileToClose) {
		if ( -e $logFile ) {
			@fstat=stat($logFile);
			if($fstat[7] >= $this->{log_maxSize}) {
				$cmd = "tail -n $this->{log_minLine} $logFile> $logFile.tmp && mv $logFile.tmp $logFile";		
				print $cmd;
				$ret = $this->runCmd("$cmd", 3);
				if (0 != $ret->{ret}) {
					print STDOUT "split $logFile failed for $ret->{desc}..";
				}
			}
		}
	}
	close($this->{hd_wf});
	close($this->{hd_nt});
}

#
#exec a command and return 
#format: ($command, $try_times)
sub runCmd {
    my ($this,$cmd, $max)   =   @_;
    my $ret_str =   "";
    my $ret     =   1;
    my $start   =   0;

    while ($start < $max) {
        $ret_str    =   `$cmd`;
        $ret        =   $?>>8;
        if ($ret != 0) {
            sleep(3);
            #print "start $start";
            $start++;
        } else {
            last;
        }
    }
    return {
        "cmd"   =>  "$cmd",
        "desc"  =>  "$ret_str",
        "ret"   =>  "$ret"
    };
}

#
#format: (class, loglevel, logstr)
sub printLog {
	my ($this, $logLevel, $logDesc)  =   @_;
	my $ret;    
	my @levelName = qw/NOTICE DEBUG WARNING FATAL/;
	my $now_time = &getNow();
	
	my $logLineNumber = (caller(0))[2];
	my $logCmd = (caller(0))[3];
	my $logRet;
	my $logCallerFunction = "";
	$logCallerFunction = (caller(1))[3];
	
	if (defined($logDesc->{cmd})) {
		$logCmd = $logDesc->{cmd};
	} else {
		$logCmd = $logCallerFunction;
	}
	if (defined($logDesc->{ret})) {
		$logRet = $logDesc->{ret};
	} else {
		$logRet = 0;
	}
	if (!defined($logCallerFunction)) {
		#如果callerFunction 为空，说明是在主脚本中调用,这里cmd赋值为包名
		$logCallerFunction = (caller(0))[0];
	}
	my ($logFileName, $path, $suffix) = fileparse((caller(0))[1]);

	my %logDetail = (
		logTime => "$now_time->{year}:$now_time->{month}:$now_time->{day} $now_time->{hour}:$now_time->{minute}:$now_time->{second}",
		logFileName => $logFileName,
		logLineNumber => $logLineNumber,
		logDesc => "$logDesc->{desc}",
		logRet  => "$logRet",
		logProg => "$this->{conf}->{logProg}",
		logPid  => $$,
		logCmd  => "$logCmd",
		logCallerFunction => "$logCallerFunction",
			
	);

	
	$ret = $this->openFile();
	#文件打开失败
	if (0 != $ret->{ret}) {
		print "open the log file failed for: $ret->{desc}\n";
		return $ret;
	} 
	
	#日志文件句柄,根据日志类型选择
	my $LOG_HD;
	#loglevel没有定义的时候，需要给初始化成warnning级别
	if (!defined($logLevel)) {
		$logLevel = $this->{WARNNING};
	}
	if ($logLevel == 2 || $logLevel == 3) {
		$LOG_HD = $this->{hd_wf};
		$logDetail{logTitle} = $levelName[$logLevel];
	} else {
		$LOG_HD = $this->{hd_nt};
		$logDetail{logTitle} = $levelName[$logLevel];
	} 

	my $logStr_part1 = "$logDetail{logTitle} : $logDetail{logTime}: $logDetail{logProg}. *  ";
	my $logStr_part2 = "$logDetail{logPid} [$logDetail{logFileName}:$logDetail{logLineNumber}] ";
	my $logStr_part3 = "taskname=[$logDetail{logProg}] cmd=[$logDetail{logCmd}] ret=[$logDetail{logRet}] ";
	my $logStr_part4 = "file=[$logDetail{logFileName}] line=[$logDetail{logLineNumber}] desc=[$logDetail{logDesc}]";
	my $logStr_part5 = "";
	my $logTmpKey;
	foreach $logTmpKey (keys (%{$logDesc})) {
		if("$logTmpKey" eq "cmd" || "$logTmpKey" eq "ret" || "$logTmpKey" eq "desc") {
			next;
		}
		$logStr_part5 .= " $logTmpKey=[$logDesc->{$logTmpKey}]";
	}

	my $logStr = "$logStr_part1"."$logStr_part2"."$logStr_part3"."$logStr_part4"."$logStr_part5"."\n";

	print {$LOG_HD}  "$logStr";
	if (1 == $this->{conf}->{printStd}) {
		print STDOUT "$logStr";
	}
	$this->closeFile();

	$ret->{ret}     =   0;
	$ret->{desc}    =   "print log file successed";
	$ret->{cmd}     =   "printLog";
	return $ret;
}

sub printNotice {
	my ($this, $logDesc) = @_;
	$this->printLog(0, "$logDesc");
}
sub disConf {
	my $this    =   shift;
	print "current_conf data:\n";
	print Dumper($this->{conf});
}

#functions for public
sub getNow {
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$sec    =   ($sec<10)?"0$sec":$sec;     #second [0,59]
	$min    =   ($min<10)?"0$min":$min;     #mintue [0,59]
	$hour   =   ($hour<10)?"0$hour":$hour;  #hour   [0,23]
	$mday   =   ($mday<10)?"0$mday":$mday;  #dayth in this month [1,31]
	$mon    =   ($mon<9)?"0".($mon+1):$mon; #month  [0,11]
	$year   +=  1900;                       #year from 1900

	#$wday the dayth in one week from sta
	#$yday the dayth in one year from 1.1
	my $weekday = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday];
	return {
		'second' => $sec,
		'minute' => $min,
		'hour'   => $hour,
		'day'    => $mday,
		'month'  => $mon,
		'year'   => $year,
		'weekNo' => $wday,
		'wday'   => $weekday,
		'yday'   => $yday,
		'date'   => "$year$mon$mday"
	};  
}
1;
