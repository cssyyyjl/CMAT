clc;close all;clear all;
s='20250611_A03';
xc=810;
yc=894;
zc=102;

r=30;
nn=60;

%%%%%%%%%%%
if (zc>=100)
        a=strcat(s,'_ch1_000',num2str(zc));
else
        if(zc>=10)
            a=strcat(s,'_ch1_0000',num2str(zc));
        else
            a=strcat(s,'_ch1_00000',num2str(zc));
        end
end
[A,M]=imread(a,'tif');
aa=im2double(A);
%%%%%%%%%

x=xc-r:1:xc+r;
[i,is]=size(x);
y=yc-r:1:yc+r;
[j,js]=size(y);

for j=1:js
    for i=1:is
        bb(j,i)=aa(y(j)+1,x(i)+1);
    end
end
bbb=bb/max(max(bb));
for j=1:js
    for i=1:is
        if(bbb(j,i)>0.5)
            bbb(j,i)=1;
        else
            bbb(j,i)=0;
        end        
    end
end
imshow(bbb);
[rows,cols]=size(bbb);
xx=ones(rows,1)*[1:cols];
yy=[1:rows]'*ones(1,cols);
area=sum(sum(bbb));
mx=round(sum(sum(bbb.*xx))/area);
my=round(sum(sum(bbb.*yy))/area);
hold on
plot(mx,my,'r+');

for i=1:is
    xxx(i)=bb(my,i);
end

for j=1:js
    yyy(j)=bb(j,mx);
end


%%%%%%%%%%%%%
z=zc-nn:zc+nn;
[n,ns]=size(z);
for n=1:1:ns
    n
    if (z(n)>=100)
        a=strcat(s,'_ch1_000',num2str(z(n)));
    else
        if(z(n)>=10)
            a=strcat(s,'_ch1_0000',num2str(z(n)));
        else
            a=strcat(s,'_ch1_00000',num2str(z(n)));
        end
    end
    [A,M]=imread(a,'tif');
    aa=im2double(A);
    
    for j=1:js
       for i=1:is
           bb(j,i)=aa(y(j)+1,x(i)+1);
       end
    end
    bbb=bb/max(max(bb));
    for j=1:js
       for i=1:is
          if(bbb(j,i)>0.5)
              bbb(j,i)=1;
          else
              bbb(j,i)=0;
          end  
       end
    end
    [rows,cols]=size(bbb);
    xx=ones(rows,1)*[1:cols];
    yy=[1:rows]'*ones(1,cols);
    area=sum(sum(bbb));
    meanx(n)=round(sum(sum(bbb.*xx))/area);
    meany(n)=round(sum(sum(bbb.*yy))/area);
    zzz(n)=bb(meany(n),meanx(n));
    
    xm=meanx(n)-20:meanx(n)+20;
    [k,ks]=size(xm);
    for k=1:ks
        zz(n,k)=aa( yc-r+meany(n),xc-r+xm(k));
    end
 

end
zz=zz/max(max(zz));
figure
imshow(zz);
cftool