require 'rubygems'
require 'selenium-webdriver'
require 'pp'

def get_general_infos(url, driver)
    driver.get(url)
    wait = Selenium::WebDriver::Wait.new(:timeout => 10)
    wait.until { driver.find_element(:xpath, '//*[@id="content-wrapper"]').displayed?  }
    nbr_followers = driver.find_element(:css, "li.list-group-item:nth-child(4) > div:nth-child(1) \
                                          > div:nth-child(2) > span:nth-child(2)").text.gsub(",", "").to_i
    nbr_subs = driver.find_element(:css, "div.g-x-wrapper:nth-child(7) > div:nth-child(1) \
                                     > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)").text.gsub(",", "").to_i
    return nbr_followers, nbr_subs
end

def get_followers_infos(url, driver)
    driver.get(url)
    wait = Selenium::WebDriver::Wait.new(:timeout => 10)
    wait.until { driver.find_element(:xpath, "/html/body/div[3]/div[4]").displayed?  }
    last_month_foll = driver.find_element(:css, "#DataTables_Table_1 > tbody:nth-child(2) > tr:nth-child(1) \
                                              > td:nth-child(3)").text.gsub(".","").gsub("M", "0000").to_i

    snd_last_month_foll = driver.find_element(:css, "#DataTables_Table_1 > tbody:nth-child(2) > tr:nth-child(2) \
                                                  > td:nth-child(3)").text.gsub(".","").gsub("M", "0000").to_i

    thrird_last_month_foll = driver.find_element(:css, "#DataTables_Table_1 > tbody:nth-child(2) > tr:nth-child(3) \
                                                     > td:nth-child(3)").text.gsub(".","").gsub("M", "0000").to_i
    return last_month_foll, snd_last_month_foll, thrird_last_month_foll
end

def get_subscribers_infos(url, driver)
    driver.get(url)
    wait = Selenium::WebDriver::Wait.new(:timeout => 10)
    wait.until { driver.find_element(:xpath, "//*[@id=\"content-wrapper\"]/div[6]").displayed?  }

    last_month_sub = driver.find_element(:css, "#subscribers > tbody > tr:nth-child(2) > td:nth-child(2) \
                                             > b").text.gsub(",","").to_i
    snd_last_month_sub = driver.find_element(:css, "#subscribers > tbody > tr:nth-child(3) > td:nth-child(2) \
                                                 > b").text.gsub(",","").to_i
    third_last_month_sub = driver.find_element(:css, "#subscribers > tbody > tr:nth-child(4) > td:nth-child(2) \
                                                   > b").text.gsub(",","").to_i
    return last_month_sub, snd_last_month_sub, third_last_month_sub
end

def get_streams_infos(url, driver)
    driver.get(url)
    wait = Selenium::WebDriver::Wait.new(:timeout => 10)
    wait.until { driver.find_element(:xpath, "/html/body/div[3]/div[4]").displayed? }

    last_stream_avg_views = driver.find_element(:css, "tr.odd:nth-child(1) > td:nth-child(3) \
                                                    > span:nth-child(1)").text.gsub(",", "").to_i
    snd_last_stream_avg_views = driver.find_element(:css, "tr.even:nth-child(2) > td:nth-child(3) \
                                                        > span:nth-child(1)").text.gsub(",", "").to_i
    third_last_stream_avg_views = driver.find_element(:css, "tr.odd:nth-child(3) > td:nth-child(3) \
                                                          > span:nth-child(1)").text.gsub(",", "").to_i
    return last_stream_avg_views, snd_last_stream_avg_views, third_last_stream_avg_views
 end

def twitch(creator)
    twitch_general = "https://twitchtracker.com/#{creator}"
    twitch_streams = "https://twitchtracker.com/#{creator}/streams"
    twitch_subs = "https://twitchtracker.com/#{creator}/subscribers"
    twitch_stats = "https://twitchtracker.com/#{creator}/statistics"

    options = Selenium::WebDriver::Chrome::Options.new
    options.add_argument('--headless') 
    options.add_argument("--log-level=OFF")
    driver = Selenium::WebDriver.for :chrome, options: options

    nbr_followers, nbr_subs = get_general_infos(twitch_general, driver)
    last_month_foll, snd_last_month_foll, thrird_last_month_foll = get_followers_infos(twitch_stats, driver)
    foll_growth_rate = (((last_month_foll.fdiv(thrird_last_month_foll))**(1/3.0) - 1) * 100).round(2)
    last_month_sub, snd_last_month_sub, third_last_month_sub = get_subscribers_infos(twitch_subs, driver)
    subs_growth_rate = (((nbr_subs.fdiv(snd_last_month_sub))**(1/3.0) - 1) * 100).round(2)
    last_stream_avg_views, snd_last_stream_avg_views, third_last_stream_avg_views = get_streams_infos(twitch_streams, driver)
    three_last_streams_avg_views = ((last_stream_avg_views + snd_last_stream_avg_views + third_last_stream_avg_views) / 3.0).to_i
    driver.quit()
    values = {
    "current # of followers" => nbr_followers,
    "# of followers of last month " => last_month_foll,
    "# of followers 2 months ago" =>  snd_last_month_foll,
    "# of followers 3 months ago" => thrird_last_month_foll,
    "Avg growth rate of new followers (%)" => foll_growth_rate,
    "current # of subscribers" => nbr_subs,
    "# of subscribers of last month " => last_month_sub,
    "# of subscribers 2 months ago" =>  snd_last_month_sub,
    "# of subscribers 3 months ago" => third_last_month_sub,
    "Avg growth rate of new subscribers on 3 last months (%)" => subs_growth_rate,
    "Avg CCr views on last stream" => last_stream_avg_views,
    "Avg CCr views on second last stream" => snd_last_stream_avg_views,
    "Avg CCr views on third last stream" => third_last_stream_avg_views,
    "Av. # of viewers on 3 last streams" => three_last_streams_avg_views
    }
    return values
end

pp twitch("pokimane")
