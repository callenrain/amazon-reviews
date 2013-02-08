#!/usr/bin/perl

# name: Amazon reviews downloader
# author: Andrea Esuli
# website: http://www.esuli.it
# date: January 2012
# license: please cite and put a link to the source if you use it. Modify and redistribute as you want.
# usage: ./downloadAmazonReviews.pl <domain> <list of IDs of amazon products>
# example: ./downloadAmazonReviews.pl com B0040JHVC2 B004CG4CN4
# output: a directory ./amazonreviews/<domain>/<ID> is created for each product ID; HTML files containing reviews are downloaded and saved in each directory.

use strict;
use LWP::UserAgent; 
use HTTP::Request;

$| = 1; #autoflush

my $ua = LWP::UserAgent->new;
$ua->timeout(10);
$ua->env_proxy;
$ua->agent('Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.91 Chrome/12.0.742.91 Safari/534.30');

mkdir "amazonreviews";

my $sleepTime = 1;

my $domain = shift;
mkdir "amazonreviews/$domain";

my $id = "";
while($id  = shift) {

    my $dir = "amazonreviews/$domain/$id";
    mkdir $dir;

    my $urlPart1 = "http://www.amazon.".$domain."/product-reviews/";
    my $urlPart2 = "/?ie=UTF8&showViewpoints=0&pageNumber=";
    my $urlPart3 = "&sortBy=bySubmissionDateDescending";

    my $referer = $urlPart1.$id.$urlPart2."1".$urlPart3;

    my $page = 1;
    my $lastPage = 1;
    while($page<=$lastPage) {

	my $url = $urlPart1.$id.$urlPart2.$page.$urlPart3;

	print $url;

	my $request = HTTP::Request->new(GET => $url);
	$request->referer($referer);

	my $response = $ua->request($request);
	if($response->is_success) {
	    print " GOTIT\n";
	    my $content = $response->decoded_content;

	    if(open(CONTENTFILE, ">./$dir/$page")) {
		print CONTENTFILE $content;
		close(CONTENTFILE);
		print "ok\t$domain\t$id\t$page\t$lastPage\n";
	    }
	    else {
		print "failed\t$domain\t$id\t$page\t$lastPage\n";
	    }

	    while($content =~ m#cm_cr_pr_top_link_([0-9]+)#gs ) {
		my $val = $1+0;
		if($val>$lastPage) {
		    $lastPage = $val;
		}
	    }
	    
	    if($sleepTime>0) {
		--$sleepTime;
	    }
	}
	else {
	    print " ERROR ".$response->code;
	    if($response->code==503) {
		--$page;
		++$sleepTime;
		print " retrying (timeout $sleepTime)\n";
	    }
	    else {
		print "\n";
	    }
	}
	++$page;
	sleep($sleepTime);
    }
}
