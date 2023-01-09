/**
  users table
 */
create table users
(
    id            int auto_increment
        primary key,
    nick_name     varchar(255)                       not null,
    email         varchar(255)                       not null,
    password      varchar(255)                       not null,
    refresh_token varchar(255) null,
    expire_time   datetime null,
    created_at    datetime default CURRENT_TIMESTAMP not null,
    updated_at    datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    constraint email
        unique (email),
    constraint nick_name
        unique (nick_name)
);

/**
  index for email
 */
create index idx_email on users (email);


/**
  histories table
 */
create table histories
(
    id         int auto_increment primary key,
    user_id    int          not null,
    detail     varchar(255) not null,
    money      int          not null default (0),
    is_deleted tinyint      not null default (0),
    created_at datetime              default CURRENT_TIMESTAMP not null,
    updated_at datetime              default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    foreign key (user_id) references users (id)
);