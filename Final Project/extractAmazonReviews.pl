#!/usr/bin/perl

# name: Amazon reviews extractor
# author: Andrea Esuli
# website: http://www.esuli.it
# date: January 2012
# license: please cite and put a link to the source if you use it. Modify and redistribute as you want.
# usage: ./extractAmazonReviews.pl <list of files downloaded with downloadAmazonReviews.pl>
# example: ./extractAmazonReviews.pl amazonreviews/B0040JHVC2/*
# output: a simple CSV to standard output

use strict;

my $filename ="";
my $count = 0;

while($filename= shift) {
    open (FILE, "<", $filename)  or  next;
    my $whole_file;
    {
	local $/;
	$whole_file = <FILE>;
    }
    close(FILE);

    $whole_file =~ m#product\-reviews/([A-Z0-9]+)/ref\=cm_cr_pr#gs;
    my $model = $1;
    
    $whole_file =~ m#table id="productReviews.*?>(.*?)</table>#gs;
    $whole_file = $1;

    while ($whole_file =~ m#-->(.*?)(<!--|$)#gs) {
	my $block = $1;
	my $end = $2;
	$block =~ m#\<div.*?star_([1-5])_([05]).*?\<b\>(.*?)\<\/b\>.*?br\>(.*?)\<\/nobr#gs;

	my $rating = $1.".".$2;
	my $title = $3;
	my $date = $4;

	$date =~ m/([a-zA-Z]+) ([0-9]+), ([0-9]+)/;
	my $month = $1;

	if($month eq "January") {
	    $month = "01";
	}
	elsif($month eq "February") {
	    $month = "02";
	}
	elsif($month eq "March") {
	    $month = "03";
	}
	elsif($month eq "April") {
	    $month = "04";
	}
	elsif($month eq "May") {
	    $month = "05";
	}
	elsif($month eq "June") {
	    $month = "06";
	}
	elsif($month eq "July") {
	    $month = "07";
	}
	elsif($month eq "August") {
	    $month = "08";
	}
	elsif($month eq "September") {
	    $month = "09";
	}
	elsif($month eq "October") {
	    $month = "10";
	}
	elsif($month eq "November") {
	    $month = "11";
	}
	elsif($month eq "December") {
	    $month = "12";
	}
	else {
	    $month = "XX";
	}

	my $newDate = "XX"; 
	if(! $month eq "XX") {
	    $newDate = sprintf ( "$3$month%02d",$2);
	}

	my $userId = "ANONYMOUS";
	if($block =~ m#profile\/(.*?)["/].*?\<\/div\>.*?\<\/div\>.#gs) {
	    $userId = $1;
	}

	$block =~ s/<p>//g;
	$block =~ s/<\/p>//g;
	$block =~ s/<br>//g;
	$block =~ s/<br \/>//g;
	$block =~ m#div>([^<]*?)<div style="padding-top#gs;
	my $review = $1;
	$review =~ s/^\s+|\s+$//g;
	$review =~ s/\n/ /g;
	$review =~ s/\r/ /g;
	$review =~ s/"/'/g;

	if(length($review) > 0) {
	    print "\"$count\",\"$newDate\",\"$model\",\"$rating\",\"$date\",\"$userId\",\"$title\",\"$review\"\n";
	}
	++$count;
    }
}
