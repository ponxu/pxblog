/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2012-12-20 17:51:07                          */
/*==============================================================*/


drop table if exists bj_post;

drop table if exists bj_post_tag;

drop table if exists bj_setting;

drop table if exists bj_tag;

/*==============================================================*/
/* Table: bj_post                                               */
/*==============================================================*/
create table bj_post
(
   id                   int not null auto_increment,
   url                  varchar(500),
   title                varchar(500) not null,
   content              longtext not null,
   addtime              int(10) not null,
   top                  int not null default 0,
   status               varchar(20) not null default 'public',
   type                 varchar(20) not null default 'post',
   password             varchar(10),
   primary key (id),
   unique key UNI_POST_URL (url)
);

/*==============================================================*/
/* Table: bj_post_tag                                           */
/*==============================================================*/
create table bj_post_tag
(
   post_id              int,
   tag_id               int
);

/*==============================================================*/
/* Table: bj_setting                                            */
/*==============================================================*/
create table bj_setting
(
   id                   int not null auto_increment,
   name                 varchar(100) not null,
   value                longtext not null,
   description          varchar(200),
   primary key (id),
   unique key UNI_SETTING_NAME (name)
);

/*==============================================================*/
/* Table: bj_tag                                                */
/*==============================================================*/
create table bj_tag
(
   id                   int not null auto_increment,
   name                 varchar(50) not null,
   sort                 int default 0,
   post_count           int default 0,
   primary key (id),
   unique key UNI_TAG_NAME (name)
);

alter table bj_post_tag add constraint FK_TO_POST foreign key (post_id)
      references bj_post (id) on delete restrict on update restrict;

alter table bj_post_tag add constraint FK_TO_TAG foreign key (tag_id)
      references bj_tag (id) on delete restrict on update restrict;

