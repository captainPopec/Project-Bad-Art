# Project-Bad-Art
An overview of methods for quantifying the amount of stimuli in daily routine of animals - Bachelor thesis

Attempt 1: How to extedn this logic to more data, does it make sens eto group data not only for bio phony and antroopohony but also for say urban sounds vs rural sounds, or house sounds, those are all different,also how can I really know that sounds pikcing is unbiased when claude did it himself., also doe sit really make sense to plot a PCA? I mean most of the metrics are in fact redundant in a way right? Did it d multiplication of median(intesnity) and variablity(entropy)? In a away that is way more usefull metric

I lost a second huge paragrapf, forgot to commit it fuckkkk

# Big thoughts
it was a huge thinking progress, most notable breakthrough was the idea to create a score that quanitfies verbosity as a key information load mettric for us humans. This will of course tip the balance into the favur of antropogenic sounds, but that is expected, the whole point is to show that modern environemnt carries way more informatio than natural ones. I donet seem to rememebr any otehr idea but I know there were some quite nice ones. AH yes, there was this talk about PCA not being very useful when I already know the hypotehism which is intensity*variability = informaition laod. So I could use PCA only as a confirmation that these two indeed do account for most difference between all sounds, not only bio vs antropo.  And SECODN IDEA was how to measure this verbostiy, obviouyl there is no limit to how many words a human can say or produce by some means, still there is a maximum in 99% cases, that valueI can use like pKh in chemistry, create a pH score out of verbosity load, say upper bound would be a eminem rapping rap god, and lower bound would be one word per same duration I guess, but there is a provlem of handling biophony, it has no words whatsoever, so it would always make verbosiyt zero, but if I can force the negative log to be 1 whenever there are now wors in audio, than I can safely multiply verbosity with intenisty and varibiliyt as it iwill not influence them at all - neutral element for multiplication.

# Hm but does this makes sense?
we kind of defeat th epurpose of overall informtion, because I think we argue from the perspective of that part of the bran that determines which stimuli pass and which dont pass into the brain. what is the ame of that?
 Thalamus ofc

# Turns ut it's a bad idea
IT makes no sense multiplying the base score with verbosity, as I already pointeed out, the verbose data would simply be in a different cluster no matetr what simply due to it's dimensionality difference. So instead of squashing it into just one score, it could be interasting perhaps to leave it as two separate dimensions, x= information y=verbostiy, so I expect 4 quadrants, low information/low verbosity, low information / high verbostiy( althouth this one might be fairly empty), high information /low verbosity, high /high